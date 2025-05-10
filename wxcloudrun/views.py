from datetime import datetime
from flask import render_template, request, requests
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """
    # 获取请求体参数
    params = request.get_json()

    # print("aaaaaaaaaa111111")
    # print("params data: " + str(params))

    # try:
    #     # 将数据转发到另一个服务器
    #     response = requests.post('http://113.200.194.122:8988/post', json=params)
        
    #     # 返回转发后的响应
    #     return make_succ_response(response.json())
    # except requests.exceptions.RequestException as e:
    #      return make_err_response('缺少action参数11' + str(params))


    # 检查action参数
    # if 'action' not in params:
    #     return make_err_response('缺少action参数22' + str(params))

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误' + str(params))


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
