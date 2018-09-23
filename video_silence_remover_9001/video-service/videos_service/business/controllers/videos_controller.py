import os
from multiprocessing import Process

from flask import send_from_directory
from werkzeug.utils import secure_filename

from crud.utils.video_editing import cut_video
from crud.video_metadata_operations import find_all_metadata, find_one_metadata, delete_one_metadata, insert_metadata, \
    update_metadata


def post_video(file):
    """Receives a file and starts cutting the silence parts of it"""
    metadata = {'stepsCompleted': 0, 'totalSteps': 5}
    insert_metadata(metadata)
    metadata['filename'] = '{}.{}'.format(str(metadata['_id']), secure_filename(file.filename))
    metadata['path'] = os.path.join(os.environ.get('NFS_DIR', '/tmp'),
                                    metadata['filename'])
    file.save(metadata['path'])
    update_metadata(metadata, metadata['_id'])
    # ** this processes are not being joined, using celery or other method would be better **
    # Would love to discuss the advantages of that approach and the disadvantages of calling cut_video in this request
    p = Process(target=cut_video, args=(metadata,))
    p.daemon = True
    p.start()
    return str(metadata['_id']), 200


def get_videos():
    """ Gets a list of all the videos"""
    return find_all_metadata(), 200


def get_video(_id):
    """Sends the converted video file"""
    metadata = find_one_metadata(_id)
    return send_from_directory(os.path.dirname(metadata['converted_path']), os.path.basename(metadata['converted_path']))


def delete_video(_id):
    """ Deletes a video from the system """
    # return delete_one_metadata(_id), 200
    return "NOT YET IMPLEMENTED", 501


def get_video_status(_id):
    """ Gets the status of the video's conversion"""
    # This endpoint will be polled by the gui for the progress of the video conversion
    # A more elegant approach would be using websockets
    v_metadata = find_one_metadata(_id)
    v_metadata.pop('path', None)
    v_metadata.pop('converted_path', None)
    return v_metadata, 200
