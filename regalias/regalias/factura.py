# GENERATE STRING FOR CODE_QR
from clientes.models import Cliente

from django.conf import settings

from users.models import Empresa

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget

import os

def get_decimal_amount(venta):
    total_str = str(venta.costo)
    array_split = total_str.split('.')
    residue = '00'
    if len(array_split) != 1:
        residue = array_split[1]
    if len(residue) == 1:
        residue += '0'
    return residue

def build_string_qr(venta, code_control):
    empresa = Empresa.objects.all().first()
    nro_autorizacion =  empresa.nro
    nit = empresa.nit
    cliente = Cliente.objects.get(pk=venta.cliente_id)

    nit = str(nit)  # nit o ci
    ndf = str(venta.nro_venta)  # numero de factura
    nda = str(nro_autorizacion)  # numero de autorizacion
    fde = str(venta.fecha.strftime('%d/%m/%Y'))  # DDMMAAA
    monto = str(venta.costo)
    ibpcf = str(venta.costo)  # TODO clarificar esta parte
    nit_c = str(cliente.nit)  # NIT/CI/CEX comprador
    i_c_t = 0
    ivng = 0
    inscf = 0
    dbr = 0
    text_value = "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s" % (
        nit, ndf, nda, fde, monto, ibpcf, code_control, nit_c, i_c_t, ivng, inscf, dbr)
    qr_code_drawing(text_value, venta.id)
    return text_value

# GENERATE AND DRAWING QR
def qr_code_drawing(text_value, name):
    qrw = QrCodeWidget(text_value)
    b = qrw.getBounds()
    w = b[2] - b[0]
    h = b[3] - b[1]
    d = Drawing(120, 120, transform=[120. / w, 0, 0, 120. / h, 0, 0])
    d.add(qrw)
    dir = settings.BASE_DIR

    d.save(formats=['png'], outDir=os.path.join(dir, 'static/barcode'), fnRoot=str(name))

#CONVERT FLOAT TO INTEGER
def conver_to_int(string):
    string = str(string)
    new = string.split('.')
    return new[0]


#GENERATE CODE CONTROL
def get_code_control(venta):
    empresa = Empresa.objects.all().first()
    nit = empresa.nit
    nro = empresa.nro
    #llave dosificacion
    key = empresa.key
    #organization = Company.objects.get(pk=billing.company.id)

    nit = str(nit)  # nit o ci
    ndf = str(venta.nro_venta)  # numero de factura
    nda = str(nro)  # numero de autorizacion
    fde = str(venta.fecha.strftime('%Y%m%d'))  # DDMMAAA
    monto = str(conver_to_int(venta.costo))
    nit_c = venta.cliente.nit  # NIT/CI/CEX comprador
    key = str(key)
    c = Code_control()
    code = c.generar(nda, ndf, nit_c, fde, monto, key)
    return code

# ALGOTIMO DE CODIGO DE CONTROL
class Code_control():
    def __init__(self):
        # Verhoeff Digit table variables
        self.table_d = ((0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                        (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
                        (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
                        (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
                        (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
                        (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
                        (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
                        (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
                        (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
                        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
                        )
        self.table_p = ((0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
                        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
                        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
                        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
                        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
                        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
                        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
                        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))
        self.table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)


    def big_base_convert(self, numero, baseconv):
        dic = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
               'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '+',
               '/']
        cociente = 1
        palabra = ''
        while cociente > 0:
            cociente = numero / baseconv
            resto = numero % baseconv
            palabra = dic[int(resto)] + palabra
            numero = cociente
        return palabra


    def swap(self, num1, num2):
        temp = num2
        num2 = num1
        num1 = temp
        return num1, num2

    def allegedrc4(self, mensaje, llaverc4):
        t, x, y, j, s = list(range(256)), 0, 0, 0, 1  # ,argv[1]
        k = llaverc4  # (map(lambda b:a to i(a[b:b+2],16), range(0,len(a),2))*256)[:256]
        strlen_llave = len(llaverc4)
        strlen_mensaje = len(mensaje)
        index1 = 0
        i = 0
        while i < 256:
            j = (int(ord(llaverc4[index1])) + t[i] + j) % 256
            # t[j], t[i]= t[i], t[j]
            aux = t[j]
            t[j] = t[i]
            t[i] = aux
            index1 = (index1 + 1) % strlen_llave
            i += 1
        cifrado = ''
        i = 0
        while i < strlen_mensaje:
            s = mensaje
            l, x = len(s), (x + 1) % 256
            y, c = (y + t[x]) % 256, int(ord(s[i]))
            t[x], t[y] = t[y], t[x]
            aux = t[x]
            t[x] = t[y]
            t[y] = aux
            nmen = c ^ t[(t[x] + t[y]) % 256]
            cadtemp = self.complete_cero(self.big_base_convert(nmen, 16))
            cifrado = cifrado + '-' + cadtemp
            i += 1
        result = cifrado[1:len(cifrado)]
        return result

    def reverse(self, cadena):
        return cadena[::-1]

    # *
    # * Digito Verhoeff
    #
    def complete_cero(self, value):
        if len(value) == 1:
            value = '0' + value
        return value

    def calcsum(self, number):
        c = 0
        n = self.reverse(number)
        length = len(n)
        nchar = list(n)
        i = 0
        while i < length:
            c = self.table_d[c][self.table_p[(i + 1) % 8][int(str(nchar[i]))]]
            i += 1
        return self.table_inv[c]

    def verhoeff_add_recursive(self, num, digits):
        temp = str(num)
        while digits > 0:
            temp += str(self.calcsum(temp))
            digits -= 1
        return temp


    def generar(self, autorizacion, numero, nitci, fecha, monto, llave):
        # paso 1
        numero = self.verhoeff_add_recursive(numero, 2)
        nitci = self.verhoeff_add_recursive(nitci, 2)
        fecha = self.verhoeff_add_recursive(fecha, 2)
        monto = self.verhoeff_add_recursive(monto, 2)

        suma = str(int(numero) + int(nitci) + int(fecha) + int(monto))
        suma = self.verhoeff_add_recursive(suma, 5)
        digitos = "" + suma[(len(suma) - 5): len(suma)]
        digitossum = [0, 0, 0, 0, 0]
        cadenas = ["", "", "", "", ""]
        inicio = 0
        x = 0
        enumerator = list(digitos)
        for enum in enumerator:
            d = enum
            digitossum[x] = int(d) + 1
            cadenas[x] = llave[inicio: int(d) + 1 + inicio]
            inicio += int(d) + 1
            x += 1

        autorizacion += cadenas[0]
        numero += cadenas[1]
        nitci += cadenas[2]
        fecha += cadenas[3]
        monto += cadenas[4]

        # paso3
        arc4 = self.allegedrc4(autorizacion + numero + nitci + fecha + monto, llave + digitos)

        # paso4
        suma_total = 0
        sumas = [0, 0, 0, 0, 0]
        strlen_arc4 = len(arc4)
        i = 0
        while i < strlen_arc4:
            x = int(ord(arc4[i]))
            sumas[i % 5] += x
            suma_total += x
            i += 1
        # paso5
        total = 0
        i = 0

        while i < len(sumas):
            total += suma_total * sumas[i] / digitossum[i]
            i += 1
        mensaje = self.big_base_convert(total, 64)

        last = self.allegedrc4(mensaje, llave + digitos)

        return last