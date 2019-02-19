import sys
import time
import sched
import shutil
import os
import constants as cons
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from controller import File

class JobScheduler(object):
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def setup(self, interval, action, actionargs=()):
        action(*actionargs)
        self.scheduler.enter(interval, 1, self.setup,
                             (interval, action, actionargs))

    def run(self):
        self.scheduler.run()


class MonitorHandler(FileSystemEventHandler):
    def on_created(self, event):  # quando um arquivo é criado

        print(f'Arquivo: {event.src_path}')

        head, tail = os.path.split(event.src_path)

        if File.valide_filename(tail):
            # executa o processamento do arquivo
            import controller
            controller.File(event.src_path).run()
        else:
            print('Nome de arquivo inválido!')


def run_job_cut():
    from controller import JobCut, ApiCut, ApiGloboPlay

    print('################################################')
    print('# Iniciando verificação de status de corte e   #')
    print('# a entrega dos vídeos já cortados.            #')
    print('################################################')
    print(' ')
    print('# Tarefa de verificação de status:')

    job = JobCut()
    list_jobs_in_progress = job.list_jobs_in_progress()
    if list_jobs_in_progress:
        for j in list_jobs_in_progress:
            print(f"- Consumindo API de status para verificar o status do corte do vídeo "
                  f"{j['cut_instruction']['title']} ...")
            if ApiCut().status(j['job_external_id']):
                print(f"- Vídeo {j['cut_instruction']['title']} já está cortado!")
                job.update_status(j['job_external_id'], cons.STATUS_COMPLETED)
            else:
                print(f"- O vídeo {j['cut_instruction']['title']} "
                      f"não está cortado, uma nova verificação será feita dentro de {cons.INTERVAL_SECONDS} segundos...")
    else:
        print('# Nada a fazer...')


    print(' ')
    print('# Tarefa de entrega de vídeos já cortados:')
    list_jobs_completed = job.list_jobs_completed()
    if list_jobs_completed:
        for j in list_jobs_completed:

            shutil.copyfile(f"{cons.PATH_VIDEO_CORTADO}arquivo_de_video.mp4", f"{cons.PATH_VIDEO_ENTREGUE}{j['path']}")

            print(f"- Consumindo API de entrega para o vídeo {j['cut_instruction']['title']} ...")
            if ApiGloboPlay(j['cut_instruction']['title'], j['cut_instruction']['duration'], j['path']).send():
                print(f"- Vídeo {j['cut_instruction']['title']} entregue com sucesso!")
                job.update_status(j['job_external_id'], cons.STATUS_DELIVERY)
    else:
        print('# Nada a fazer...')

    print(' ')
    print('################################################')
    print('# FIM DA TAREFA                                #')
    print('################################################')


def create_app():
    try:
        path = sys.argv[1] if len(sys.argv) > 1 else '.'

        # processando os arquivos que já estão no diretório quando a aplicação é iniciada
        files = os.listdir(f'{sys.path[0]}/{path}')
        for f in files:
            if File.valide_filename(f):  # valida o nome do arquivo de acordo com o padrão
                if not File.search_filename(f):  # procura o nome do arquivo no db, se não encontrar processa o arquivo
                    print('processar arquivo...')
                    File(f'{path}/{f}').run()  # processando o arquivo

        # para monitorar se um novo arquivo é adicionado no diretório
        event_handler = MonitorHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        # para verificar a cada X segundos os Jobs de corte
        periodic_scheduler = JobScheduler()
        periodic_scheduler.setup(cons.INTERVAL_SECONDS, run_job_cut)
        periodic_scheduler.run()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    create_app()
