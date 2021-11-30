# coding: UTF-8
#
# 상태 불명의 노드를 클러스터에서 제거
#
import signal, os, sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from time import sleep

uk_node = {}  # KEY는 상태 불명이 된 노드의 이름, 값은 카운트

## 정지 요청 시그널 처리
def handler(signum, frame):
    sys.exit(0)

## 노드 제거 함수
def node_delete(v1,name):
    body = client.V1DeleteOptions()
    try:
        resp = v1.delete_node(name, body)
        print("delete node %s done" % name)
    except ApiException as e:
        print("Exception when calling CoreV1Api->delete_node: %s\n" % e)

## 노드 감시 함수
def node_monitor(v1):
    try:
        ret = v1.list_node(watch=False)
        for i in ret.items:
            n_name = i.metadata.name
            #print("%s" % (i.metadata.name)) #디버그 용
            for j in i.status.conditions:
                #print("\t%s\t%s" % (j.type, j.status)) #디버그 용
                if (j.type == "Ready" and j.status != "True"):
                    if n_name in uk_node:
                        uk_node[n_name] += 1
                    else:
                        uk_node[n_name] = 0
                    print("unknown %s  count=%d" % (n_name,uk_node[n_name]))
                    # 카운터가 3회 넘어서면 노드를 제거
                    if uk_node[n_name] > 3:
                        del uk_node[n_name]
                        node_delete(v1,i.metadata.name)
                # 1번이라도 상태가 돌아오면 카운터를 초기화
                if (j.type == "Ready" and j.status == "True"):
                    if n_name in uk_node:
                        del uk_node[n_name]
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_node: %s\n" % e)

## 메인
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handler) # 시그널 처리
    config.load_incluster_config()         # 인증 정보 취득
    v1 = client.CoreV1Api()                # 인스턴스화
    # 감시 루프
    while True:
        node_monitor(v1)
        sleep(5) # 감시 간격
