from fpdf import FPDF
import datetime as dt
import os


def export_invoice(output_file: str, total_price: float, tva: float, seller: str, customer: str, footer: str):
    """
    Exportation de la facture sous forme d'un fichier PDF.

    :param output_file: Chemin du fichier de sortie.
    :param total_price: Prix toutes charges comprises.
    :param tva: Part de la TVA à appliquer entre 0 et 1.
    :param seller: Coordonnées du vendeur.
    :param customer: Coordonnées du client.
    :param footer: Formule de fin de page.
    """
    # Paramètres du document
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_lang('FR')
    pdf.add_page()
    ubuntu_path = os.path.join(os.path.dirname(__file__), 'fonts/Ubuntu/Ubuntu-Regular.ttf')
    pdf.add_font(family='Ubuntu-Regular', fname=ubuntu_path)
    pdf.set_font(family='Ubuntu-Regular', size=14)

    # Corps du document
    pdf.multi_cell(0, None, seller); pdf.ln()
    pdf.cell(None, None, f"Le {dt.datetime.now().strftime('%d/%m/%Y')}"); pdf.ln(); pdf.ln()
    pdf.multi_cell(0, None, customer); pdf.ln()
    pdf.cell(None, None, "DOIT"); pdf.ln(); pdf.ln()

    def insert_points(begin: str, end: str) -> str:
        pw = pdf.get_string_width('.')
        aw = pdf.get_string_width(begin+end)
        n_points = int((pdf.epw - aw) // pw)
        return begin + ('.' * n_points) + end

    tva_price = total_price * tva
    tht_price = round(total_price - tva_price, 2)
    tva_price = round(tva_price, 2)
    total_price = round(total_price, 2)
    pdf.cell(None, None, insert_points('TOTAL HORS TAXES', f'{tht_price:.2f}€')); pdf.ln()
    pdf.cell(None, None, insert_points(f'TVA {int(tva*100)}%', f'{tva_price:.2f}€')); pdf.ln()
    pdf.cell(None, None, insert_points('TOTAL T.T.C.', f'{total_price:.2f}€')); pdf.ln(); pdf.ln()

    pdf.multi_cell(0, None, footer)

    # Enregistrement du document
    pdf.output(output_file)
