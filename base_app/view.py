from flask import Blueprint, render_template, \
request, flash, redirect, url_for, session, Response
from .resources.s3 import S3

inst_s3 = S3()
base_view = Blueprint("base_view", __name__, url_prefix='/bucket', template_folder='templates', static_folder='static')

@base_view.route("/", methods=["GET", "POST"])
def index_buckets():
    if session.get('content_object'): session.pop('content_object')

    if request.method == "GET":
        buckets= inst_s3.list_all_buckets()
        return render_template('buckets.html', buckets=buckets)
    if request.method == "POST":
        bucket_name = request.form['bucket_name'] # inst_s3.get_bucket_name()
        return redirect(url_for('base_view.index_objects', bucket_name=bucket_name))

@base_view.route("/<bucket_name>", methods=["GET", "POST"])
def index_objects(bucket_name, content_object=''):
    if session.get('content_object'): content_object=session['content_object']

    objects = inst_s3.list_all_objects(bucket_name)
    return render_template('objects.html', bucket_name=bucket_name, objects=objects, content_object=content_object)

@base_view.route("/<bucket_name>/read", methods=["POST"])
def read(bucket_name):
    ''' get content from a file in the bucket'''
    key = request.form['key']
    bucket_name = inst_s3.get_bucket_name()
    content_object = inst_s3.get_object(bucket_name, key)

    flash('File read successfully')
    session['content_object'] = content_object
    session['key'] = key
    return redirect(url_for('base_view.index_objects', bucket_name=bucket_name))

@base_view.route('/<bucket_name>/delete', methods=['POST'])
def delete(bucket_name):
    ''' delete an object from a file in the bucket '''
    key = request.form['key']

    bucket_name = inst_s3.get_bucket_name()
    status_delete = inst_s3.delete_object(bucket_name, key)

    if (status_delete >= 200 or status_delete < 300):
        flash('File deleted successfully')

    return redirect(url_for('base_view.index_objects', bucket_name=bucket_name))

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

@base_view.route("/<bucket_name>/update", methods=["POST"])
def update(bucket_name, key=None):
    ''' get content from a file in the html and update it in bucket file '''
    if session.get('key'): key=session['key']
    content_object = request.form['content_object']

    bucket_name = inst_s3.get_bucket_name()
    status_update = inst_s3.put_object(bucket_name, key, content_object)

    if status_update:
        flash('File updated successfully')

    session['content_object'] = content_object
    return redirect(url_for('base_view.index_objects', bucket_name=bucket_name))