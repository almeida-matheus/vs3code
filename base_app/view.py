from flask import Blueprint, render_template, \
request, flash, redirect, url_for, session, Response
from .resources.s3 import S3

inst_s3 = S3()

base_view = Blueprint("base_view", __name__, url_prefix='/s3', template_folder='templates', static_folder='static')

@base_view.route("/", methods=["GET", "POST"])
def index(content_object=''):
    if session.get('content_object'): content_object=session['content_object']
    bucket_name = inst_s3.get_bucket_name()
    objects = inst_s3.list_all_objects(bucket_name)
    return render_template('index.html', bucket_name=bucket_name, objects=objects, content_object=content_object)

@base_view.route('/delete', methods=['POST'])
def delete():
    ''' delete an object from a file in the bucket '''
    key = request.form['key']

    bucket_name = inst_s3.get_bucket_name()
    status_delete = inst_s3.delete_object(bucket_name, key)

    if (status_delete >= 200 or status_delete < 300):
        flash('File deleted successfully')

    return redirect(url_for('base_view.index'))

@base_view.route("/read", methods=["POST"])
def read():
    ''' get content from a file in the bucket'''
    key = request.form['key']
    bucket_name = inst_s3.get_bucket_name()
    content_object = inst_s3.get_object(bucket_name, key)

    flash('File read successfully')
    session['content_object'] = content_object
    session['key'] = key
    return redirect(url_for('base_view.index'))

@base_view.route("/download", methods=["POST"])
def download():
    ''' get content from a file in the bucket and download it'''
    key = request.form['key']
    bucket_name = inst_s3.get_bucket_name()
    file_obj_content = inst_s3.download_object(bucket_name, key)

    flash('File download successfully')
    return Response(
        file_obj_content,
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )

@base_view.route("/update", methods=["POST"])
def update(key=None):
    ''' get content from a file in the html and update it in bucket file '''
    if session.get('key'): key=session['key']
    content_object = request.form['content_object']

    bucket_name = inst_s3.get_bucket_name()
    status_update = inst_s3.put_object(bucket_name, key, content_object)

    if status_update:
        flash('File updated successfully')

    session['content_object'] = content_object
    return redirect(url_for('base_view.index'))