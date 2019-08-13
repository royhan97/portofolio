import os
from flask import render_template, redirect, send_file, \
    url_for, request, session, flash
from .make import create_pattern
from .utils import digest_params, send_email, session_check


""" RETURN PAGES """
def index_page():
    return render_template('pages/index.html')


def build_page():
    return render_template('pages/build.html')


def order_page():
    if not session_check('img_id'): return redirect('/')
    
    img_id = session['img_id']
    return render_template('pages/order.html', img_id=img_id)


def result_design_page():
    if not session_check('img_id'): return redirect('/')

    img_id = session['img_id']
    return render_template('pages/result_design.html', img_id=img_id)


def result_order_page():
    if not session_check('order'): return redirect('/')
    if not session_check('design'): return redirect('/')

    order = session['order']
    design = session['design']

    data = {
        'order': order,
        'design': design,
    }

    return render_template('pages/result_order.html', data=data)


""" PROCEED FORM SUBMIT """
def submit_design(request):
    produk = request.form['produk']
    jumlah = int(request.form['jumlah'])
    monumen = request.form['monumen']
    motif = request.form['motif']

    if not digest_params(produk, jumlah, monumen, motif):
        return redirect('/build')

    img_id = create_pattern(produk, monumen, motif)

    data = {
        'produk': produk,
        'jumlah': jumlah,
        'monumen': monumen,
        'motif': motif,
    }

    session['design'] = data
    session['img_id'] = img_id

    return redirect(url_for('result_design_page'))


def submit_order(request):
    nama = request.form['nama']
    telp = request.form['telp']
    alamat = request.form['alamat']
    email = request.form['email']

    # TODO:
    # validate the user inputs

    data = {
        'nama': nama,
        'telp': telp,
        'alamat': alamat,
        'email': email,
    }

    session['order'] = data

    return redirect(url_for('result_order_page'))


""" OTHERS """
def finish(mail):
    # send_email(mail)
    session.clear()
    flash(True)

    return redirect('/')


def get_image(img_id):
    folder = 'static/img/patterns'
    images = os.path.join(os.getcwd(), folder,
                          'result_{}.png'.format(img_id))

    return send_file(images, mimetype='image/png')
