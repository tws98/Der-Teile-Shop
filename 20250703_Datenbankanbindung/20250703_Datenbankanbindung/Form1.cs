using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;


namespace _20250703_Datenbankanbindung
{
    public partial class Form1 : Form
    {
        string name = "";
        string vorname = "";
        string email = "";
        string suche = "";

        public class DBVerbindung
        {
            private MySqlConnection connection;

            // Verbindungskette: Server = IP oder Hostname, Database = Name deiner DB, User, Passwort
            private string connectionString = "server=10.80.0.206;database=team04;uid=team04;pwd=5VVDV;";

            public MySqlConnection VerbindungHerstellen()
            {
                connection = new MySqlConnection(connectionString);
                try
                {
                    connection.Open();
                    return connection;
                }
                catch (MySqlException ex)
                {
                    MessageBox.Show("Verbindungsfehler: " + ex.Message);
                    return null;
                }
            }

            public void VerbindungSchließen()
            {
                if (connection != null)
                    connection.Close();
            }
        }

        public Form1()
        {
            InitializeComponent();
        }

        private void bn_Speichern_Click(object sender, EventArgs e)
        {
            name = tb_Name.Text;
            vorname = tb_Vorname.Text;
            email = tb_Email.Text;

            DBVerbindung db = new DBVerbindung();
            MySqlConnection conn = db.VerbindungHerstellen();

            if (conn != null)
            {
                string sql = "INSERT INTO `kunden` (`IDKunde`, `Anrede`, `Vorname`, `Name`, `Straße`, `Hausnummer`, `OrtID`, `Telefon`, `Geburtsdatum`, `Email`, `Titel`) VALUES (NULL, '1', @vorname, @name, '', '', '1', '', '0000-00-00', @email, '');";
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                cmd.Parameters.AddWithValue("@name", name);
                cmd.Parameters.AddWithValue("@vorname", vorname);
                cmd.Parameters.AddWithValue("@email", email);

                try
                {
                    cmd.ExecuteNonQuery();
                    MessageBox.Show("Datensatz gespeichert!");
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Fehler: " + ex.Message);
                }

                db.VerbindungSchließen();
            }
        }

        private void DatenLaden()
        {
            lib_Datensaetze.Items.Clear(); // Vorherige Einträge entfernen

            DBVerbindung db = new DBVerbindung();
            MySqlConnection conn = db.VerbindungHerstellen();

            if (conn != null)
            {
                string sql = "SELECT * FROM kunden";
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                MySqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    string eintrag = $"Name: {reader["name"]} | Vorname: {reader["vorname"]} | Email: {reader["email"]}";
                lib_Datensaetze.Items.Add(eintrag);
                }

                reader.Close();
                db.VerbindungSchließen();
            }
        }

        private void btnSuchen_Click(object sender, EventArgs e)
        {
            suche = tb_Suchen.Text;

            lib_Datensaetze.Items.Clear();

            DBVerbindung db = new DBVerbindung();
            MySqlConnection conn = db.VerbindungHerstellen();

            if (conn != null)
            {
                string sql = "SELECT * FROM kunden WHERE name LIKE @suche";
                MySqlCommand cmd = new MySqlCommand(sql, conn);
                cmd.Parameters.AddWithValue("@suche", "%" + suche + "%");

                MySqlDataReader reader = cmd.ExecuteReader();

                while (reader.Read())
                {
                    string eintrag = $"Name: {reader["name"]} | Vorname: {reader["vorname"]} | Email: {reader["email"]}";
                    lib_Datensaetze.Items.Add(eintrag);
                }

                reader.Close();
                db.VerbindungSchließen();
            }
        }

        private void bn_Suchen_Click(object sender, EventArgs e)
        {
            DatenLaden();
            btnSuchen_Click(null,null);
        }
    }



    
}


