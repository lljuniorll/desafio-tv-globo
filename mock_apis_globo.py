import hug
import uuid
import random


@hug.post('/corte')
def corte(body):
    return {"message": "success", "job_id": f"{uuid.uuid4()}"}


@hug.get('/status/{job_id}')
def status(job_id):
    status = ('in_progress', 'completed')
    return {"message": "success", "status": random.choice(status), "job_id": job_id}


@hug.post('/entrega')
def entrega(body):
    return {"message": "success"}


if __name__ == '__main__':
    corte.interface.cli()