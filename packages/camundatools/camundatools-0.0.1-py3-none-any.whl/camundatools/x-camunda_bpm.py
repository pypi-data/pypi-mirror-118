import logging
import socket

import settings
from camundatools.base_rest import BaseRest

logger = logging.getLogger(__name__)


class CamundaBpm(BaseRest):
    """
    Interface para comunicação com a API do Camunda
    Documentação: https://docs.camunda.org/manual/latest/reference/
    """

    def assumir_atividade(self, task_id, username):
        super().not_empty(task_id, 'task_id')
        super().not_empty(username, 'username')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_ASSUMIR_ATIVIDADE
        url = url.replace('{id}', task_id)
        headers = self.get_header()
        data = {
            'userId': username,
        }
        return super().call('post', url, headers, data)

    def devolver_atividade(self, task_id):
        super().not_empty(task_id, 'task_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_DEVOLVER_ATIVIDADE
        url = url.replace('{id}', task_id)
        headers = self.get_header()
        return super().call('post', url, headers)

    def alterar_atividade(self, task_id, dados):
        super().not_empty(task_id, 'task_id')
        super().not_empty(dados, 'dados')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_ALTERAR_ATIVIDADE
        url = url.replace('{id}', task_id)
        headers = self.get_header()
        return super().call('put', url, headers, dados)

    def delegar_atividade(self, task_id, username):
        super().not_empty(task_id, 'task_id')
        super().not_empty(username, 'username')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_DELEGAR_ATIVIDADE
        url = url.replace('{id}', task_id)
        headers = self.get_header()
        data = {
            'userId': username,
        }
        return super().call('post', url, headers, data)

    def obter_atividades_ativas_por_variavel(self, process_keys, pesquisa, candidate_groups=None, pagina=None, count=False, filtro_atividade=None):
        super().not_empty(process_keys, 'process_keys')
        super().not_empty(pesquisa, 'pesquisa')
        super().not_list(process_keys, 'process_keys')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_ATIVIDADES

        if count:
            url += '/count'

        max_results = settings.CAMUNDA_TASK_LIST_RESULTS_PER_PAGE if pagina is not None else settings.CAMUNDA_TASK_LIST_MAX_RESULTS
        first_result = (pagina - 1) * max_results if pagina is not None and pagina > 1 else 0

        param = f'?maxResults=' + str(max_results) \
                + f'&firstResult=' + str(first_result)

        data = {
            'processDefinitionKeyIn': process_keys,
            'processVariables': pesquisa,
            'active': True,
            'sorting': self.ordem,
        }
        if filtro_atividade:
            data['taskDefinitionKey'] = filtro_atividade

        if candidate_groups:
            data['candidateGroups'] = candidate_groups

        headers = self.get_header()
        return super().call('post', url + param, headers, data)

    def query_atividades_ativas(self, or_queries, pagina=None, count=False):
        super().not_empty(or_queries, 'or_queries')
        super().not_list(or_queries, 'or_queries')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_ATIVIDADES

        if count:
            url += '/count'

        max_results = settings.CAMUNDA_TASK_LIST_RESULTS_PER_PAGE if pagina is not None else settings.CAMUNDA_TASK_LIST_MAX_RESULTS
        first_result = (pagina - 1) * max_results if pagina is not None and pagina > 1 else 0

        param = f'?maxResults=' + str(max_results) \
                + f'&firstResult=' + str(first_result)

        data = {
            'active': True,
            'orQueries': or_queries,
            'sorting': self.ordem,
        }
        headers = self.get_header()
        return super().call('post', url + param, headers, data)

    def obter_tarefas_externas(self, process_key, worker_id, topic_name, business_key=None):
        super().not_empty(process_key, 'process_key')
        super().not_empty(worker_id, 'worker_id')
        super().not_empty(topic_name, 'topic_name')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_OBTEM_TAREFAS_EXTERNAS
        headers = self.get_header()

        data = {
            'workerId': worker_id,
            'maxTasks': settings.CAMUNDA_WORKER_MAX_TASKS,
            'topics': [{
                'processDefinitionKey': process_key,
                'topicName': topic_name,
                'lockDuration': settings.CAMUNDA_WORKER_LOCK_DURATION_IN_MILISECONDS,
            }]
        }

        if settings.AMBIENTE == 'DESENVOLVIMENTO' or settings.AMBIENTE == 'TESTE':
            data['topics'][0]['processVariables'] = {'ambiente': socket.gethostname()}

        if business_key is not None:
            data['topics'][0]['businessKey'] = business_key

        return super().call('post', url, headers, data)

    def obter_tarefa_externa(self, id_processo):
        super().not_empty(id_processo, 'id_processo')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_TAREFAS_EXTERNAS
        headers = self.get_header()
        data = {
            'processInstanceId': id_processo,
        }
        return super().call('post', url, headers, data, ignore_cache=True)

    def listar_tarefas_externas(self, process_key=None, not_locked=True, with_retries=False):
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_TAREFAS_EXTERNAS
        headers = self.get_header()
        data = {
            'notLocked': not_locked,
            'withRetriesLeft': with_retries,
        }
        tasks = cache.get('tarefas_externas')
        if not tasks:
            tasks = super().call('post', url, headers, data, ignore_cache=True)
            cache.set('tarefas_externas', tasks, settings.REST_CACHE_TIMEOUT)

        if process_key is not None:
            tasks = list(filter(lambda t: t['processDefinitionKey'] == process_key, tasks))

        return tasks

    def completar_tarefa_externa(self, task_id, worker_id, variables):
        super().not_empty(task_id, 'task_id')
        super().not_empty(worker_id, 'worker_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_COMPLETAR_TAREFA_EXTERNA
        url = url.replace('{id}', task_id)
        headers = self.get_header()
        data = {
            'workerId': worker_id,
            'variables': variables,
        }
        cache.delete('variaveis_' + str(task_id))
        super().call('post', url, headers, data)

    def obter_formulario_inicial(self, process_key):
        super().not_empty(process_key, 'process_key')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_FORMULARIO_INICIAL
        url = url.replace('{key}', process_key)
        headers = self.get_header()
        return super().call('get', url, headers)

    def obter_formkey_inicial(self, process_key):
        super().not_empty(process_key, 'process_key')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_FORMKEY_INICIAL
        url = url.replace('{key}', process_key)
        headers = self.get_header()
        return super().call('get', url, headers)

    def obter_formulario_atividade(self, task_id):
        super().not_empty(task_id, 'task_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_FORMULARIO_ATIVIDADE
        url = url.replace('{id}', task_id)
        headers = self.get_header()
        return super().call('get', url, headers)

    def obter_identidades(self, task_id):
        super().not_empty(task_id, 'task_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_IDENTIDADES
        url = url.replace('{id}', task_id)
        headers = self.get_header()

        ret = cache.get('identidades_' + str(task_id))
        if ret is None:
            ret = super().call('get', url, headers, silent=True)
            cache.set('identidades_' + str(task_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)

        return ret

    def obter_diagrama(self, process_id):
        super().not_empty(process_id, 'process_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_GET_XML
        url = url.replace('{id}', process_id)
        headers = self.get_header()
        ret = cache.get('diagrama_xml_' + str(process_id))
        if ret is None:
            ret = super().call('get', url, headers, ignore_cache=True)
            cache.set('diagrama_xml_' + str(process_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)
        return ret

    def obter_variavel_processo(self, process_id, ignore_cache=False):
        super().not_empty(process_id, 'process_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_OBTER_VARIAVEL_PROCESSO
        url = url.replace('{id}', process_id) + '?deserializeValues=false'
        headers = self.get_header()
        ret = cache.get('variaveis_processo_' + str(process_id)) if not ignore_cache else None
        if ret is None:
            ret = super().call('get', url, headers, ignore_cache=True)
            cache.set('variaveis_processo_' + str(process_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)
        return ret

    def versao(self):
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_VERSAO
        headers = self.get_header()
        return super().call('get', url, headers, ignore_cache=self.ignore_cache)

    def liberar_tarefa_externa(self, external_task_id):
        super().not_empty(external_task_id, 'external_task_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LIBERAR_TAREFA_EXTERNA
        url = url.replace('{id}', external_task_id)
        headers = self.get_header()
        return super().call('post', url, headers, {})

    def registrar_falha_tarefa_externa(self, external_task_id, worker_id, mensagem, detalhes, retry):
        super().not_empty(external_task_id, 'external_task_id')
        super().not_empty(worker_id, 'worker_id')
        super().not_empty(mensagem, 'mensagem')
        super().not_empty(detalhes, 'detalhes')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_HANDLE_EXTERNAL_TASK_FAILURE
        url = url.replace('{id}', external_task_id)
        headers = self.get_header()
        data = {
            'workerId': worker_id,
            'errorMessage': mensagem,
            'errorDetails': detalhes,
            'retries': retry,
            'retryTimeout': settings.CAMUNDA_WORKER_RETRY_TIMEOUT,
        }
        return super().call('post', url, headers, data)

    def listar_incidentes(self, id_incidente=None, id_processo=None):
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LIST_INCIDENTS
        param = '?sortBy=processDefinitionId&sortOrder=asc'

        if id_incidente is not None:
            param = param + '&incidentId=' + id_incidente
        if id_processo is not None:
            param = param + '&processInstanceId=' + id_processo

        headers = self.get_header()
        return super().call('get', url + param, headers, ignore_cache=True)

    def resolver_incidente(self, id_incidente):
        super().not_empty(id_incidente, 'id_incidente')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_RESOLVE_INCIDENT
        url = url.replace('{id}', id_incidente)
        headers = self.get_header()
        return super().call('delete', url, headers)

    def set_retries(self, external_task_id, retries):
        super().not_empty(external_task_id, 'external_task_id')
        super().not_empty(retries, 'retries')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_SET_RETRIES
        url = url.replace('{id}', external_task_id)
        headers = self.get_header()
        data = {
            'retries': retries,
        }
        return super().call('put', url, headers, data)

    def listar_historico(self, process_instance):
        super().not_empty(process_instance, 'process_instance')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_HISTORICO
        param = '?processInstanceId=' + process_instance + '&sortBy=occurrence&sortOrder=desc'
        headers = self.get_header()

        atividades = ['serviceTask', 'userTask', 'startEvent', 'endEvent', 'noneEndEvent']
        lista = list(filter(lambda h: h['activityType'] in atividades, super().call('get', url + param, headers)))
        lista = sorted(lista, key=lambda task: task['startTime'], reverse=True)

        return lista

    def listar_historico_completo(self, process_instance):
        super().not_empty(process_instance, 'process_instance')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_HISTORICO
        param = '?processInstanceId=' + process_instance + '&sortBy=occurrence&sortOrder=desc'
        headers = self.get_header()
        return super().call('get', url + param, headers)

    def obter_variavel_historico(self, process_id, variavel=None):
        super().not_empty(process_id, 'process_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_OBTER_VARIAVEL_HISTORICO
        param = '?processInstanceId=' + process_id

        if variavel is not None:
            param = param + '&variableName=' + variavel

        headers = self.get_header()

        ret = cache.get('variaveis_historico_' + str(process_id)) if variavel is None else None
        if ret is None:
            ret = super().call('get', url + param, headers, ignore_cache=True)
            if variavel is None:
                cache.set('variaveis_historico_' + str(process_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)

        if variavel is not None:
            return ret[0]['value'] if ret and len(ret) >= 1 else None

        return ret

    def listar_identidades_historico(self, process_key, task_id):
        super().not_empty(process_key, 'process_key')
        super().not_empty(task_id, 'task_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_LISTAR_IDENTIDADE_HISTORICO
        param = '?taskId=' + task_id + '&processDefinitionKey=' + process_key
        headers = self.get_header()
        return super().call('get', url + param, headers)

    def reiniciar_processo(self, definition_id, process_id, atividade_inicial):
        super().not_empty(definition_id, 'definition_id')
        super().not_empty(process_id, 'process_id')
        super().not_empty(atividade_inicial, 'atividade_inicial')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_REINICIAR_PROCESSO
        url = url.replace('{id}', definition_id)
        headers = self.get_header()
        dados = {
            'processInstanceIds': [process_id],
            'instructions': [
                {
                  "type": "startBeforeActivity",
                  "activityId": atividade_inicial
                }
              ],
        }
        return super().call('post', url, headers, dados)

    def obter_instancia_historico(self, process_id):
        super().not_empty(process_id, 'process_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_OBTER_INSTANCIA_HISTORICO
        url = url.replace('{id}', process_id)
        headers = self.get_header()

        ret = cache.get('instancias_'+str(process_id))
        if ret is None:
            ret = super().call('get', url, headers)
            cache.set('instancias_'+str(process_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)

        return ret

    def obter_instancia_historico_por_business_key(self, process_key, business_key):
        """ Pode retornar mais de uma instancia, ja que um business_key pode ter mais de uma execucao
            Ex: Processo Reativado
        """
        super().not_empty(process_key, 'process_key')
        super().not_empty(business_key, 'business_key')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_OBTER_INSTANCIA_HISTORICO
        url = url.replace('/{id}', '')
        headers = self.get_header()
        data = {
            'processDefinitionKey': process_key,
            'processInstanceBusinessKey': business_key,
        }
        ret = cache.get('instancias_'+str(business_key))
        if ret is None:
            ret = super().call('post', url, headers, data)
            cache.set('instancias_'+str(business_key), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)

        return ret

    def modificar_variavel(self, process_id, nome_variavel, valor, tipo):
        super().not_empty(process_id, 'process_id')
        super().not_empty(nome_variavel, 'nome_variavel')
        super().not_empty(tipo, 'tipo')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_ALTERAR_VARIAVEL_PROCESSO
        url = url.replace('{id}', process_id)
        url = url.replace('{varName}', nome_variavel)
        headers = self.get_header()

        dados = {
            'value': valor,
            'type': tipo,
        }

        return super().call('put', url, headers, dados)

    def enviar_mensagem(self, nome_mensagem, business_key, process_id=None, variaveis=None):
        super().not_empty(business_key, 'business_key')
        super().not_empty(nome_mensagem, 'nome_mensagem')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_ENVIAR_MENSAGEM
        headers = self.get_header()

        if settings.AMBIENTE == 'DESENVOLVIMENTO' or settings.AMBIENTE == 'TESTE':
            if variaveis is None:
                variaveis = {}
            variaveis['ambiente'] = {'value': socket.gethostname(), 'type': 'String'}

        dados = {
            'messageName': nome_mensagem,
            'businessKey': business_key,
            'processInstanceId': process_id,
            'processVariables': variaveis,
        }

        return super().call('post', url, headers, dados)

    def carregar_definicoes_cmmn(self, id_definicao=None):
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_LISTAR_DEFINICOES
        param = '?latestVersion=true'

        if id_definicao is not None:
            url += '/' + id_definicao

        headers = self.get_header()

        ret = cache.get('definicoes_'+str(id_definicao))
        if ret is None:
            ret = super().call('get', url + param, headers)
            cache.set('definicoes_'+str(id_definicao), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)

        return ret

    def iniciar_caso_cmmn(self, case_key, business_key, variables):
        super().not_empty(case_key, 'case_key')
        super().not_empty(business_key, 'business_key')

        # Verifica se ja nao existe um caso com este id
        processos = self.listar_instancias_por_business_key(case_key, business_key)
        if processos:
            raise Exception(f'Já existe um caso com o id {business_key}')

        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_INICIAR_PROCESSO
        url = url.replace('{key}', case_key)
        headers = self.get_header()

        if settings.AMBIENTE == 'DESENVOLVIMENTO' or settings.AMBIENTE == 'TESTE':
            variables['ambiente'] = {'value': socket.gethostname(), 'type': 'String'}

        data = {
            'businessKey': business_key,
            'variables': variables,
        }
        return super().call('post', url, headers, data)

    def listar_instancias_cmmn(self, case_key, business_key=None):
        super().not_empty(case_key, 'case_key')

        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_LISTAR_INSTANCIAS
        param = '?caseDefinitionKey='+case_key

        if business_key is not None:
            param = param + '&businessKey=' + str(business_key)

        headers = self.get_header()
        return super().call('get', url + param, headers)

    def obter_instancia_cmmn(self, case_id):
        super().not_empty(case_id, 'case_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_OBTER_INSTANCIA
        url = url.replace('{id}', case_id)
        headers = self.get_header()

        ret = cache.get('instancias_'+str(case_id))
        if ret is None:
            ret = super().call('get', url, headers)
            cache.set('instancias_'+str(case_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)

        return ret

    def obter_instancia_historico_cmmn(self, case_id):
        super().not_empty(case_id, 'case_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_OBTER_INSTANCIA_HISTORICO
        url = url.replace('{id}', case_id)
        headers = self.get_header()

        ret = cache.get('instancias_'+str(case_id))
        if ret is None:
            ret = super().call('get', url, headers)
            cache.set('instancias_'+str(case_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)

        return ret

    def obter_variavel_cmmn(self, case_id, ignore_cache=False):
        super().not_empty(case_id, 'case_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_OBTER_VARIAVEL_PROCESSO
        url = url.replace('{id}', case_id) + '?deserializeValues=false'
        headers = self.get_header()
        ret = cache.get('variaveis_caso_' + str(case_id)) if not ignore_cache else None
        if ret is None:
            ret = super().call('get', url, headers, ignore_cache=True)
            cache.set('variaveis_caso_' + str(case_id), ret, settings.CAMUNDA_REQUEST_CACHE_TIMEOUT)
        return ret

    def modificar_variavel_cmmn(self, case_id, nome_variavel, valor, tipo):
        super().not_empty(case_id, 'case_id')
        super().not_empty(nome_variavel, 'nome_variavel')
        super().not_empty(tipo, 'tipo')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_ALTERAR_VARIAVEL_PROCESSO
        url = url.replace('{id}', case_id)
        url = url.replace('{varName}', nome_variavel)
        headers = self.get_header()

        dados = {
            'value': valor,
            'type': tipo,
        }

        return super().call('put', url, headers, dados)

    def obter_atividades_cmmn(self, case_key, business_key=None):
        super().not_empty(case_key, 'case_key')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_LISTAR_PENDENCIAS
        headers = self.get_header()
        data = {
            'caseDefinitionKey': case_key,
            'active': True,
        }
        if business_key:
            data['businessKey'] = business_key

        return super().call('post', url, headers, data)

    def iniciar_atividade_cmmn(self, execution_id, variables=None):
        super().not_empty(execution_id, 'execution_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_INICIAR_CASO
        url = url.replace('{id}', execution_id)
        headers = self.get_header()
        data = {'variables': variables} if variables else None
        return super().call('post', url, headers, data)

    def completar_atividade_cmmn(self, execution_id, variables=None):
        super().not_empty(execution_id, 'execution_id')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_COMPLETAR_CASO
        url = url.replace('{id}', execution_id)
        headers = self.get_header()
        data = {'variables': variables} if variables else None
        return super().call('post', url, headers, data)

    def excluir_instancia_cmmn(self, process_instance):
        super().not_empty(process_instance, 'process_instance')
        url = settings.CAMUNDA_API_BASE_URL + settings.CAMUNDA_API_CMMN_TERMINAR_CASO
        headers = self.get_header()
        data = {
            'id': process_instance,
        }
        return super().call('post', url, headers, data)