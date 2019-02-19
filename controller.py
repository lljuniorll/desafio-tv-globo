from model import CutInstruction, CutInstructionSchema, CutJob, CutJobSchema, CutFile, CutFileSchema, session
import datetime
import requests
import os
import re
import constants as cons

cut_instruction_schema = CutInstructionSchema()
cut_file_schema = CutFileSchema()
cut_job_schema = CutJobSchema()


class File:
    def __init__(self, file):
        self._file = file

    @property
    def file(self):
        return self._file

    @property
    def first_line_to_read(self):
        return self._first_line_to_read

    def run(self):

        file_to_read = open(self.file, "r")
        head, tail = os.path.split(self.file)

        line_number = 1
        start_line = self.number_last_line(tail)
        for line in file_to_read:
            if line_number > start_line:
                formatted_line = self.extract_line_data(line)
                show = TvShow(formatted_line).save()  # grava instruções de corte no banco de dados

                # verifica se a instrução de corte é maior que 30 segundos
                if TvShow.qualify_video_by_duration(show.duration):
                    # envia a solicitação de corte para a API externa e recebe o ID do job de corte
                    path = f"{show.id}_{str(show.reconcile_key).replace(' ', '_').strip().lower()}.mp4"
                    job_external_id = ApiCut().send(show.start_time, show.end_time, path)
                    job_cut = JobCut()
                    job_cut.save(job_external_id, path, show)

            line_number += 1
        file_to_read.close()  # fecha o arquivo

        # grava as informações arquivo no banco de dados

        filename_date_and_sequence = self.filename_date_and_sequence(tail)
        self.log_file_processing(tail, line_number-1, filename_date_and_sequence['filename_date'],
                                 filename_date_and_sequence['filename_sequence'])

    @staticmethod
    def search_filename(filename):
        file = session.query(CutFile).filter_by(filename=filename).first()
        result = cut_file_schema.dump(file).data
        return result

    @staticmethod
    def valide_filename(filename):
        regex = '[0-9]{8}(?:_)[0-9]{6}(.txt)$'
        return True if re.match(regex, filename, flags=0) else False

    @staticmethod
    def filename_date_and_sequence(filename):
        result = {'filename_date': filename[:8], 'filename_sequence': filename[9:15]}
        return result

    @staticmethod
    def extract_line_data(line):
        formatted_line = {'start_time': line[5:29].strip(), 'end_time': line[29:52].strip(),
                          'title': line[106:139].strip(), 'duration': line[184:196].strip(),
                          'reconcile_key': line[279:312].strip()}
        return formatted_line

    @staticmethod
    def filename_sequence_date():
        consulta = session.query(CutFile).order_by(CutFile.id.desc()).first()
        result = cut_file_schema.dump(consulta).data
        return int(result['last_line']) if result else 8

    @staticmethod
    def number_last_line(filename):
        consulta = session.query(CutFile).filter_by(filename=filename).order_by(CutFile.filename_sequence.desc()).first()
        result = cut_file_schema.dump(consulta).data
        return int(result['last_line']) if result else 8

    @staticmethod
    def log_file_processing(filename, last_line, filename_date, filename_sequence):
        try:
            session.add(CutFile(filename, last_line, filename_date, filename_sequence))
            session.commit()
            return True
        except:
            return False

    @property
    def list(self):
        files = session.query(CutFile).all()
        result = cut_file_schema.dump(files, many=True).data
        return result


class TvShow:
    def __init__(self, instruction):
        self._instruction = instruction

    @property
    def instruction(self):
        return self._instruction

    # TODO arrumar o try
    def save(self):
        try:
            record = CutInstruction(self.instruction['start_time'], self.instruction['end_time'],
                                    self.instruction['title'], self.instruction['duration'],
                                    self.instruction['reconcile_key'])
            session.add(record)
            session.commit()
            return record
        except:
            print(f'Erro ao tentar salvar {self.instruction}')
            return False

    @property
    def list(self):
        contato = session.query(CutInstruction).all()
        result = cut_instruction_schema.dump(contato, many=True).data
        return result

    @staticmethod
    def qualify_video_by_duration(duration):
        duration = duration[:-3]
        duration = datetime.datetime.strptime(duration, '%H:%M:%S')
        interval = datetime.datetime.strptime(cons.DURATION_MIN, '%H:%M:%S')
        return True if duration > interval else False


class JobCut:

    @staticmethod
    def save(job_external_id, path, cut):
        try:
            session.add(CutJob(job_external_id, path, cut))
            session.commit()
            return True
        except:
            return False

    @staticmethod
    def update_status(job_external_id, status):
        job = session.query(CutJob).filter_by(job_external_id=job_external_id).first()
        job.status = status
        result = cut_job_schema.dump(job).data
        session.commit()
        return result

    @staticmethod
    def list_jobs_in_progress():
        job = session.query(CutJob).filter_by(status=cons.STATUS_IN_PROGRESS).all()
        result = cut_job_schema.dump(job, many=True).data
        return result

    @staticmethod
    def list_jobs_completed():
        job = session.query(CutJob).filter_by(status=cons.STATUS_COMPLETED).all()
        result = cut_job_schema.dump(job, many=True).data
        return result

    @staticmethod
    def list_all_jobs():
        jobs = session.query(CutJob).all()
        result = cut_job_schema.dump(jobs, many=True).data
        return result


class ApiCut:

    @staticmethod
    def send(start_time, end_time, path):
        response = requests.post(cons.URL_API_CUT, json={'start_time': start_time,
                                                         'end_time': end_time, 'path': path})
        if response.status_code == 200:
            response = response.json()
            return response['job_id']
        else:
            return None

    @staticmethod
    def status(job_id):
        response = requests.get(f'{cons.URL_API_STATUS}/{job_id}')
        if response.status_code == 200:
            response = response.json()
            if response['status'] == cons.STATUS_COMPLETED:
                return True
            else:
                return False
        else:
            return False


class ApiGloboPlay:

    def __init__(self, title, duration, path):
        self._title = title
        self._duration = duration
        self._path = path

    def send(self):
        response = requests.post(cons.URL_API_DELIVERY, json={'title': self._title,
                                                              'duration': self._duration, 'path': self._path})
        if response.status_code == 200:
            response = response.json()
            return True
        else:
            return False
