# * import libraries
import os

# * import agent
from agent import AgentCRUD

def addAllFiles(path:str):
    '''
    Recursively retrieve all PDF files from a parent folder

    :param path: parent path
    :return: list of dict (PDF file info)
    '''

    agent = AgentCRUD()

    files_pdf = []

    for file in os.listdir(path):
        tempo_files = agent.loadDoc(f'{path}/{file}', 'admin/comptable')
        tempo_list = files_pdf + tempo_files
        files_pdf.clear()
        files_pdf = tempo_list

    agent.saveDoc(files_pdf)


if __name__ == '__main__':
    addAllFiles('drive/Factures')