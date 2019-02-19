INTERVAL_SECONDS = 10  # tempo em segundos para verificação do status de corte
DURATION_MIN = '00:00:30'  # duração de referência para qualificar um vídeo para corte, a duração deverá ser maior
STATUS_IN_PROGRESS = 'in_progress'  # status inicial dos Jobs
STATUS_COMPLETED = 'completed'  # status do termino do Job de corte
STATUS_DELIVERY = 'delivery'  # status que o vídeo foi cortado e entregue
URL_API_CUT = 'http://localhost:8000/corte'  # url da api de corte do vídeo
URL_API_STATUS = 'http://localhost:8000/status'  # url da api que retorna o status do job de corte do vídeo
URL_API_DELIVERY = 'http://localhost:8000/entrega'  # url da api para entrega do vídeo cortado
TABLE_CUT_INSTRUCTION = 'cut_instruction'  # nome da tabela de instruções de corte
TABLE_CUT_JOB = 'cut_job'  # nome da tabela dos trabalhos de corte
TABLE_CUT_FILE = 'cut_file'  # nome da tabela que armazena as informações dos arquivos de corte
PATH_VIDEO_CORTADO = 'videos-cortados/'  # caminho para os vídeos cortados
PATH_VIDEO_ENTREGUE = 'videos-entregues/'  # caminho para mover os vídeos entregues

