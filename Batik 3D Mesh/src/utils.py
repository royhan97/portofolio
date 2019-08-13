from flask import session
from flask_mail import Message


def digest_params(produk, jumlah, monumen, motif):
    """ Check if all params are allowed """

    list_produk = ['fabric', 'shawl']
    list_jumlah = list(range(1, 11))
    list_monumen = ['lawang-sewu', 'tugu-muda', 'blenduk']
    list_motif = ['truntum', 'parang', 'ceplok']

    if produk not in list_produk \
            or jumlah not in list_jumlah \
            or monumen not in list_monumen \
            or motif not in list_motif:
        return False

    return True


def send_email(mail):
    sender = '<some email>'

    msg = Message('Pemesanan Berhasil',
                  sender=sender,
                  recipients=[session['order']['email']])
    msg_to_sender = Message('Ada Pesanan',
                            sender=sender,
                            recipients=[sender])

    msg.body = 'Hai, ' + session['order']['nama'] + '\n\n'
    msg.body += 'Pesanan kamu berhasil diterima.\n\n'
    msg.body += 'Detail pesanan:\n'
    msg.body += 'Nama: {}\n'.format(session['order']['nama'])
    msg.body += 'Email: {}\n'.format(session['order']['email'])
    msg.body += 'Nomor: {}\n'.format(session['order']['telp'])
    msg.body += 'Alamat: {}\n'.format(session['order']['alamat'])
    msg.body += 'Produk: {}\n'.format(session['design']['produk'])
    msg.body += 'Jumlah: {}\n'.format(session['design']['jumlah'])
    msg.body += 'Monumen: {}\n'.format(session['design']['monumen'])
    msg.body += 'Motif: {}\n\n'.format(session['design']['motif'])
    msg.body += 'Terima kasih.'

    msg_to_sender.body = msg.body

    mail.send(msg)
    mail.send(msg_to_sender)

    return True


def session_check(param):
    if session.get(param) is None:
        return False

    return True
