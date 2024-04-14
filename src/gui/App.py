import os
import tkinter as tk
from core.dataframe import DataFrame
from core.schema import WallboxSchema
from gui.config import parse_config
from tomli import TOMLDecodeError
from PIL import Image, ImageTk
import tkinter.filedialog as fd
from gui.ScrollableFrame import ScrollableFrame
from core.data_operators import load_data, agg_user, agg_total
from core.exceptions import WallboxCurrencyError, WallboxSchemaError
from gui.invoice import export_invoice


class App(tk.Tk):
    """
    Interface utilisateur de l'application.
    * Chargement d'un fichier csv.
    * Agrégation de la table.
    * Exportation des résultats.
    """
    def __init__(self, config_file: str):
        """
        :param config_file: Chemin du fichier de configuration TOML.
        """
        super().__init__()
        self.title("Wallbox Express")
        ico_path = os.path.join(os.path.dirname(__file__), 'assets/icon.png')
        ico = ImageTk.PhotoImage(Image.open(ico_path))
        self.wm_iconphoto(False, ico)

        # Dataset modifié par les callbacks
        self.df = DataFrame()

        # Deux agrégations possibles
        self.agg_counter = 2

        # Lignes à supprimer
        self.deselected_rows = set()

        # Sélection du fichier CSV
        self.filewindow = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.filewindow.pack(side=tk.TOP, expand=False, fill=tk.X)
        self.labelfile = tk.Label(self.filewindow, text="Aucun fichier sélectionné", font=("Helvetica", 12, "normal"))
        self.browsebutton = tk.Button(self.filewindow, text="Parcourir", font=("Helvetica", 12, "normal"),
                                      command=self.browse_file)
        self.browsebutton.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
        self.labelfile.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=10)

        # Visualisation de la table de données
        self.frame = ScrollableFrame(self)
        self.tablewindow = self.frame.scrollable_frame
        self.frame.pack(side=tk.TOP, expand=False, fill=tk.BOTH)

        # Actions sur la table de données
        self.actionswindow = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.actionswindow.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH)
        self.filterbutton = tk.Button(self.actionswindow, text="Filtrer", font=("Helvetica", 12, "normal"),
                                      command=self.drop_rows)
        self.aggbutton = tk.Button(self.actionswindow, text="Agréger", font=("Helvetica", 12, "normal"),
                                   command=self.agg_data)
        self.exportbutton = tk.Button(self.actionswindow, text="Exporter", font=("Helvetica", 12, "normal"),
                                      command=self.export_file)
        self.invoicebutton = tk.Button(self.actionswindow, text="Facture", font=("Helvetica", 12, "normal"),
                                       command=self.export_invoice)
        self.filterbutton.pack(side=tk.LEFT, padx=(5, 0), pady=5)
        self.aggbutton.pack(side=tk.LEFT, padx=(5, 0), pady=5)
        self.exportbutton.pack(side=tk.LEFT, padx=(5, 0), pady=5)
        self.invoicebutton.pack(side=tk.LEFT, padx=(5, 0), pady=5)

        # Chargement de la configuration
        try:
            self.config = parse_config(config_file)
        except TOMLDecodeError:
            self.print_error("Erreur : Le parsing du fichier de configuration a échoué.")
        except AssertionError:
            self.print_error("Erreur : Des champs du fichier de configuration sont manquants.")
        except:
            self.print_error("Erreur : Une erreur inattendue est survenue.")

    def print_error(self, error_msg: str):
        """
        Affiche un message d'erreur

        :param error_msg: Message à afficher.
        """
        self.empty_table()
        tk.Label(self.tablewindow, text=error_msg, font=("Helvetica", 12, "normal"), fg="red").pack()

    def empty_table(self):
        """
        Vide la table d'affichage du dataset.
        """
        # Suppression des éléments de tablewindow
        for child in self.tablewindow.winfo_children():
            child.destroy()

        # Réinitialisation des filtres de ligne
        self.deselected_rows = set()

    def print_table(self):
        """
        Affiche le dataset sous forme d'une table.
        """
        self.empty_table()

        # Noms des colonnes
        columns = self.df.columns
        tk.Label(self.tablewindow).grid(row=0, column=0)
        for j in range(len(columns)):
            entry = tk.Entry(self.tablewindow, width=len(columns[j]) + 5, font=("Helvetica", 10, "bold"))
            entry.insert(tk.END, columns[j])
            entry.configure(state=tk.DISABLED)
            entry.configure({"disabledforeground": "black"})
            entry.grid(row=0, column=j+1, sticky='w')

        # Affichage de chaque ligne
        for i in range(len(self.df)):
            # Application partielle pour copier i dans la fermeture
            checkbutton = tk.Checkbutton(self.tablewindow, command=(lambda i: (lambda: self.select_rows(i)))(i))
            checkbutton.select()  # Par défaut on garde toutes les lignes
            checkbutton.grid(row=i+1, column=0)
            for j in range(len(columns)):
                entry = tk.Entry(self.tablewindow, width=len(columns[j]) + 5, font=("Helvetica", 10, "normal"))
                entry.insert(tk.END, self.df[i][j])
                entry.configure(state=tk.DISABLED)
                entry.configure({"disabledforeground": "black"})
                entry.grid(row=i+1, column=j+1, sticky='w')

    def select_rows(self, index: int):
        """
        Supprime ou rajoute une ligne dans le dataset.

        :param index: Numéro de ligne.
        """
        if index in self.deselected_rows:
            self.deselected_rows.remove(index)
        else:
            self.deselected_rows.add(index)

    def drop_rows(self):
        """
        Supprime définitivement les lignes du dataset et affiche la table.
        """
        if len(self.df) == 0:
            self.print_error("Erreur : Veuillez charger un fichier.")
            return

        self.df.drop_lines(self.deselected_rows)
        self.deselected_rows = set()
        self.print_table()

    def browse_file(self):
        """
        Met à jour le dataset en chargeant un fichier csv et affiche la table.
        """
        filepath = fd.askopenfilename(title="Ouvrir un fichier CSV", filetypes=[('Fichiers CSV', '.csv')])
        if len(filepath) >= 1:
            # Mise à jour du nom de fichier
            self.labelfile.config(text=os.path.basename(filepath))

            try:
                # Chargement de la table
                currency = self.config["schema"]["currency"]
                self.df = load_data(filepath, currency)
                # Affichage de la table
                self.print_table()
                # Réinitialisation du bouton d'agrégation
                self.agg_counter = 2

            except FileNotFoundError:
                self.print_error("Erreur : Le fichier est introuvable")
            except WallboxSchemaError:
                self.print_error("Erreur : Le schéma de données est incorrect")
            except WallboxCurrencyError:
                self.print_error(f"Erreur : La monnaie ({currency}) est inconsistante")
            except:
                self.print_error("Erreur : Une erreur inattendue est survenue")

    def export_file(self):
        """
        Exporte le dataset sous forme d'un fichier csv.
        """
        if len(self.df) == 0:
            self.print_error("Erreur : Veuillez charger un fichier.")
            return

        filepath = fd.asksaveasfilename(title="Exporter un fichier CSV", filetypes=[('Fichiers CSV', '.csv')],
                                        defaultextension='.csv')
        if len(filepath) >= 1:
            self.df.write_csv(filepath)

    def export_invoice(self):
        """
        Exporte la ligne du total final sous forme d'un document PDF.
        """
        if len(self.df) != 1:
            self.print_error("Erreur : Veuillez agréger la table.")
            return

        filepath = fd.asksaveasfilename(title="Exporter un fichier PDF", filetypes=[('Fichiers PDF', '.pdf')],
                                        defaultextension='.pdf')
        if len(filepath) >= 1:
            cost_index = self.df.headers[WallboxSchema.COST.target_name]
            export_invoice(filepath, 
                           total_price=self.df[0][cost_index], 
                           tva=self.config["invoice"]["tva"],
                           seller=self.config["invoice"]["seller"], 
                           customer=self.config["invoice"]["customer"],
                           footer=self.config["invoice"]["footer"])

    def agg_data(self):
        """
        Met à jour le dataset en réalisant l'agrégation et affiche la table.
        """
        if len(self.df) == 0:
            self.print_error("Erreur : Veuillez charger un fichier.")
            return
        elif self.agg_counter == 0:
            return
        elif self.agg_counter == 2:
            self.df = agg_user(self.df)
        elif self.agg_counter == 1:
            self.df = agg_total(self.df)
        self.agg_counter -= 1
        self.print_table()
