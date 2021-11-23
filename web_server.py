from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import numpy as np

def buildMatix(R:int, C:int, Z:int):
    if (R > 0) and (C > 0) and (0 < Z <= 1000000):
        matrix = np.array([[Z + r for c in range(C)] for r in range(R)], dtype=np.int32)
        return (matrix, "Matrix built successfully")

    return (0, "Invalid parameters: R, C, Z -> ({}, {}, {})".format(R,C,Z))

def getSumMatrixByCoord(matrix:np.ndarray, X:int, Y:int):
    R, C = matrix.shape
    if (0 <= X <= R) and (0 <= Y <= C):
        subMatrix = matrix[0:Y + 1, 0:X + 1]
        print(matrix, matrix.shape)
        print(subMatrix, subMatrix.shape)
        return (int(subMatrix.sum()), 'Matrix Summation Successful')

    return (0, "Invalid parameters: X, Y -> ({}, {})".format(X, Y))

# Genera 456.976.000 Combinaciones de Patentes con su respectivo ID (Resultado de: 26^4*10^3)
def buildPatentsMethod01(returnDB:bool=True, saveDB:bool=False, fileDB:str='patentsDB.json'):
    starTimeBuild = datetime.now()
    print("{} | Patents construction start time".format(
        starTimeBuild.strftime('%Y-%m-%d %H:%M:%S')
    ))
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    patents = {}
    domains = []
    for l0 in ALPHABET:
        for l1 in ALPHABET:
            for l2 in ALPHABET:
                for l3 in ALPHABET:
                    domains.append(l0 + l1 + l2 + l3)
    patentID = 0
    for domain in domains:
        for n in range(1000):
            patent = '{}{}'.format(domain, str(n).zfill(3))
            patentID += 1
            patents[patent] = patentID

    timeDurationBuild = datetime.now().timestamp() - starTimeBuild.timestamp()
    print("{}: Duration time to build patents: {} Sec".format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), timeDurationBuild
    ))
    print('{} | Total patents built: {}'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        len(patents)
    ))

    if saveDB and isinstance(fileDB, str):
        starTimeSaveDB = datetime.now()
        print("{} | Patents DB save start time".format(
            starTimeSaveDB.strftime('%Y-%m-%d %H:%M:%S')
        ))

        f = open(fileDB, 'a')
        json.dump(patents, f)
        f.close()

        timeDurationSaveDB = datetime.now().timestamp() - starTimeSaveDB.timestamp()
        print("{}: Duration time to save patents DB: {} Sec".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), timeDurationSaveDB
        ))

    if returnDB: return patents

# Genera 26.000 Combinaciones de Patentes con su respectivo ID (Resultado de: 26*10^3)
def buildPatentsMethod02(returnDB:bool=True, saveDB:bool=False, fileDB:str='patentsDB.json'):
    starTimeBuild = datetime.now()
    print("{} | Patents construction start time".format(
        starTimeBuild.strftime('%Y-%m-%d %H:%M:%S')
    ))
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    patents = {}
    domains = [l * 4 for l in ALPHABET]
    patentID = 0
    for domain in domains:
        for n in range(1000):
            patent = '{}{}'.format(domain, str(n).zfill(3))
            patentID += 1
            patents[patent] = patentID

    timeDurationBuild = datetime.now().timestamp() - starTimeBuild.timestamp()
    print("{}: Duration time to build patents: {} Sec".format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), timeDurationBuild
    ))
    print('{} | Total patents built: {}'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        len(patents)
    ))

    if saveDB and isinstance(fileDB, str):
        starTimeSaveDB = datetime.now()
        print("{} | Patents DB save start time".format(
            starTimeSaveDB.strftime('%Y-%m-%d %H:%M:%S')
        ))

        f = open(fileDB, 'a')
        json.dump(patents, f)
        f.close()

        timeDurationSaveDB = datetime.now().timestamp() - starTimeSaveDB.timestamp()
        print("{}: Duration time to save patents DB: {} Sec".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), timeDurationSaveDB
        ))

    if returnDB: return patents

def loadPatentsFromDBFile(fileDB:str):
    starTimeLoad = datetime.now()
    print("{} | Patents load start time".format(
        starTimeLoad.strftime('%Y-%m-%d %H:%M:%S')
    ))

    if os.path.exists(fileDB): patents = json.loads(open(fileDB).read())
    else: patents = {}

    timeDurationLoad = datetime.now().timestamp() - starTimeLoad.timestamp()
    print("{}: Duration time to load patents: {} Sec".format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), timeDurationLoad
    ))
    print('{} | Total patents load: {}'.format(
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        len(patents)
    ))

    return patents

baseDir = os.path.dirname(os.path.abspath(__file__)) + os.sep
appConf = json.loads(open(baseDir + 'config/app_cfg.json').read())
if appConf['DB'] == 'LOAD': patentsDB = loadPatentsFromDBFile(fileDB=baseDir + 'db/patentsDB.json')
elif appConf['DB'] == 'BUILD':
    if appConf['DBBuildMethod'] == 1: # Genera 456.976.000 Combinaciones de Patentes con la forma AAAA000 excluyendo la Ñ
        patentsDB = buildPatentsMethod01(saveDB=True, fileDB=baseDir + 'db/patentsDB.json')
    elif appConf['DBBuildMethod'] == 2: # Genera 26.000 Combinaciones de Patentes con la forma AAAA000 excluyendo la Ñ
        patentsDB = buildPatentsMethod02(saveDB=True, fileDB=baseDir + 'db/patentsDB.json')
else: patentsDB = {}

app = Flask(__name__)

@app.route('/patent-domain/<domain>', methods=['GET'])
def patent_by_domain(domain=None):
    global patentsDB

    try:
        if domain != None:
            patentId = patentsDB.get(domain, 0)
            if patentId > 0:
                response = {
                    "mssg": "Patent found",
                    "patentId": patentId
                }
            else:
                response = {
                    "mssg": "Patent not found",
                    "patentId": patentId
                }
        else:
            response = {
                "mssg": "Invalid domain: {}".format(domain),
                "patentId": 0
            }
    except Exception as e:
        response = {
            "mssg": "An error has occurred ({})".format(e.args),
            "patentId": 0
        }

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/patent-id/<id>', methods=['GET'])
def patent_by_id(id=None):
    global patentsDB

    try:
        if id != 0:
            patentId = int(id)
            patentDomain = [domain for domain, id in patentsDB.items() if id == patentId]

            if len(patentDomain) > 0:
                response = {
                    "mssg": "Patent ID found",
                    "patentDomain": patentDomain[0]
                }
            else:
                response = {
                    "mssg": "Patent ID not found",
                    "patentDomain": 0
                }
        else:
            response = {
                "mssg": "Invalid id: {}".format(id),
                "patentDomain": None
            }
    except Exception as e:
        response = {
            "mssg": "An error has occurred ({})".format(e.args),
            "patentDomain": None
        }

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/matrix-sum', methods=['POST'])
def matrix_sum():
    params = request.get_json()

    try:
        if isinstance(params, dict) and all(key in params.keys() for key in ['R', 'C', 'Z', 'X', 'Y']):
            buildResult = buildMatix(params['R'], params['C'], params['Z'])
            if isinstance(buildResult[0], np.ndarray):
                matrix = buildResult[0]
                sumResult = getSumMatrixByCoord(matrix, params['X'], params['Y'])
                if sumResult[0] > 0:
                    response = {
                        "mssg": sumResult[1],
                        "sum": sumResult[0]
                    }
                else:
                    response = {
                        "mssg": sumResult[1],
                        "sum": sumResult[0]
                    }
            else:
                response = {
                    "mssg": buildResult[1],
                    "sum": buildResult[0]
                }
        else:
            response = {
                "mssg": "Invalid parameters",
                "sum": 0
            }
    except Exception as e:
        response = {
            "mssg": "An error has occurred ({})".format(e.args),
            "sum": 0
        }

    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=False)