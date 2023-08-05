import requests
import docker
from hurry.filesize import size
from numpy import mean
import re
import typer

# Set up docker client
client = docker.from_env()
running_containers = client.containers.list()
# set Prometheus url
PROMETHEUS = 'http://localhost:9090/'
# create a typer app
app = typer.Typer()

# set thresholds for each metrics
CPU_THRESHOLD_1 = 20
CPU_THRESHOLD_2 = 30
DISK_THRESHOLD = 500
MEM_THRESHOLD = 500

# use the queries values to query key metrics
queries = {'MEM': 'container_memory_usage_bytes{job=~"cadvisor", id=~"/docker/.*"}',
           'CPU': ['rate(container_cpu_usage_seconds_total{job=~"cadvisor", id =~ "/docker/.*"} [10m]) *100',
                   'rate(container_cpu_usage_seconds_total{job=~"cadvisor", id =~ "/docker/.*"} [20m]) *100',
                   'rate(container_cpu_usage_seconds_total{job=~"cadvisor", id =~ "/docker/.*"} [30m]) *100'],
           'DISK': 'container_fs_writes_bytes_total{job=~"cadvisor", id=~"/docker/.*"}',
           'NETWORK': 'rate(container_network_transmit_bytes_total[10m])'
           }

# dict to save queried metrics for further using
queried_metrics = {}

container_names = [x.name for x in client.containers.list()]
container_id = [x.id for x in client.containers.list()]


@app.command()
def list_containers():
    for c in client.containers.list():
        print("id: {id},name: {name}".format(id=c.id, name=c.name))


@app.command()
def container(con_name):
    con_id = 0
    if con_name not in container_names:
        raise NameError("invalid container name")
    con_id = client.containers.get(con_name).id
    query_metrics(con_id)


@app.command()
def app_logs():
    response = requests.get(PROMETHEUS + '/api/v1/query',
                            params={'query': 'ERROR_FATAL_COUNTER'})
    results = response.json()['data']['result']
    values = sum([int(r.get('value')[1]) for r in results])
    print('{error_num} Errors detected during App running!'.format(error_num = values))
    for result in results:
        log_type = result.get('metric').get('log_type')
        error_message = result.get('metric').get('error_message')
        error_num = result.get('value')[1]

        print('Log type: {log_type}\nNumber of Errors: {error_num}\nError message: {error_message}\n*-----------------*'.
              format(error_num=error_num, log_type=log_type, error_message=error_message))


def query_metrics(con_id):
    for key in queries.keys():
        response = requests.get(PROMETHEUS + '/api/v1/query',
                                params={'query': queries.get(key)})
        results = response.json()['data']['result']
        network_id = client.networks.list('chemdo_default')[0].short_id
        if key == 'CPU':
            cpu_values = []
            cpu_core_values = []
            for query in queries.get(key):
                response = requests.get(PROMETHEUS + '/api/v1/query',
                                        params={'query': query})
                results = response.json()['data']['result']
                for result in results:
                    if result.get('metric').get('id').split("/")[2] == con_id:
                        cpu_core_values.append(float(result.get('value')[0]))
                        cpu_values.append(mean([float(i) for i in cpu_core_values]))

            queried_metrics['CPU'] = cpu_values[0]
            print('{metric}: {value}%, ({value_20_mins}%), ({value_30_mins}%)'
                  .format(metric=key,
                          value='{:.2f}'.format(
                              cpu_values[0]),
                          value_20_mins='{:.2f}'.format(
                              cpu_values[1]),
                          value_30_mins='{:.2f}'.format(
                              cpu_values[2])))
            # alerting
            if cpu_values[0] > CPU_THRESHOLD_1:
                print('threshold was reached in the last 10 minutes!')
        if key == 'MEM':
            for result in results:
                if result.get('metric').get('id').split("/")[2] == con_id:
                    queried_metrics['MEM'] = size(int(result.get('value')[1]))
                    print('{metric}: {value}'.format(metric=key, value=queried_metrics.get(key)))
        if key == 'DISK':
            for result in results:
                if result.get('metric').get('id').split("/")[2] == con_id:
                    queried_metrics['DISK'] = size(int(result.get('value')[1]))
                    print('{metric}: {value}'.format(metric=key, value=queried_metrics.get(key)))
        if key == 'NETWORK':
            for result in results:
                if result.get('metric').get('interface').split("-")[1][:len(network_id)] == network_id:
                    queried_metrics['NETWORK'] = size(int(float(result.get('value')[1])))
                    print('{metric}: {value}'.format(metric=key, value=queried_metrics.get(key)))
                    break
    # check status for this container
    status = ''
    if int(re.findall(r'\d+', queried_metrics.get('MEM'))[0]) > MEM_THRESHOLD or float(queried_metrics.get(
            'CPU')) > CPU_THRESHOLD_1 or int(re.findall(r'\d+', queried_metrics.get('DISK'))[0]) > DISK_THRESHOLD \
            or float(re.findall(r'\d+', queried_metrics.get('NETWORK'))[0]) == 0:
        status = 'Warning'
    if float(queried_metrics.get('CPU')) > CPU_THRESHOLD_2:
        status = 'FATAL'
    else:
        status = 'OK'
    print('Status of this container is: {status}'.format(status=status))

    # list_containers
    # query_by_name_id(con_name='prometheus')

    # cpu core? or average
    # Network: total traffic in the last 1 min or the average traffic per second in the last 1 min
    # Warning Criterian for all of the Metrics including Network

    # response = requests.get(PROMETHEUS + '/api/v1/query', params={'query': queries.get('CPU')})
    # results=response.json()['data']['result']
    # for result in results:
    #     print(result)

    #
    # while command != 'quit':
    #     command = input()
    #     if command not in command_list:
    #         raise NameError('command not found')
    #     query_str = command_query.get(command)

    # end_of_month = datetime.datetime.today().replace(day=1).date()
    #
    # last_day = end_of_month - datetime.timedelta(days=1)
    # duration = '[' + str(last_day.day) + 'd]'
    # print('{:%B %Y}:'.format(last_day))
