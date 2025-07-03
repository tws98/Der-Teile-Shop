namespace _20250703_Datenbankanbindung
{
    partial class Form1
    {
        /// <summary>
        /// Erforderliche Designervariable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Verwendete Ressourcen bereinigen.
        /// </summary>
        /// <param name="disposing">True, wenn verwaltete Ressourcen gelöscht werden sollen; andernfalls False.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Vom Windows Form-Designer generierter Code

        /// <summary>
        /// Erforderliche Methode für die Designerunterstützung.
        /// Der Inhalt der Methode darf nicht mit dem Code-Editor geändert werden.
        /// </summary>
        private void InitializeComponent()
        {
            this.tb_Name = new System.Windows.Forms.TextBox();
            this.lb_Name = new System.Windows.Forms.Label();
            this.lb_Vorname = new System.Windows.Forms.Label();
            this.tb_Vorname = new System.Windows.Forms.TextBox();
            this.bn_Speichern = new System.Windows.Forms.Button();
            this.lb_Email = new System.Windows.Forms.Label();
            this.tb_Email = new System.Windows.Forms.TextBox();
            this.lib_Datensaetze = new System.Windows.Forms.ListBox();
            this.tb_Suchen = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.lb_Namesuchen = new System.Windows.Forms.Label();
            this.bn_Suchen = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // tb_Name
            // 
            this.tb_Name.Location = new System.Drawing.Point(173, 63);
            this.tb_Name.Name = "tb_Name";
            this.tb_Name.Size = new System.Drawing.Size(100, 22);
            this.tb_Name.TabIndex = 0;
            // 
            // lb_Name
            // 
            this.lb_Name.AutoSize = true;
            this.lb_Name.Location = new System.Drawing.Point(26, 69);
            this.lb_Name.Name = "lb_Name";
            this.lb_Name.Size = new System.Drawing.Size(47, 16);
            this.lb_Name.TabIndex = 1;
            this.lb_Name.Text = "Name:";
            // 
            // lb_Vorname
            // 
            this.lb_Vorname.AutoSize = true;
            this.lb_Vorname.Location = new System.Drawing.Point(26, 107);
            this.lb_Vorname.Name = "lb_Vorname";
            this.lb_Vorname.Size = new System.Drawing.Size(65, 16);
            this.lb_Vorname.TabIndex = 2;
            this.lb_Vorname.Text = "Vorname:";
            // 
            // tb_Vorname
            // 
            this.tb_Vorname.Location = new System.Drawing.Point(173, 104);
            this.tb_Vorname.Name = "tb_Vorname";
            this.tb_Vorname.Size = new System.Drawing.Size(100, 22);
            this.tb_Vorname.TabIndex = 3;
            // 
            // bn_Speichern
            // 
            this.bn_Speichern.Location = new System.Drawing.Point(84, 224);
            this.bn_Speichern.Name = "bn_Speichern";
            this.bn_Speichern.Size = new System.Drawing.Size(88, 31);
            this.bn_Speichern.TabIndex = 4;
            this.bn_Speichern.Text = "Speichern";
            this.bn_Speichern.UseVisualStyleBackColor = true;
            this.bn_Speichern.Click += new System.EventHandler(this.bn_Speichern_Click);
            // 
            // lb_Email
            // 
            this.lb_Email.AutoSize = true;
            this.lb_Email.Location = new System.Drawing.Point(29, 144);
            this.lb_Email.Name = "lb_Email";
            this.lb_Email.Size = new System.Drawing.Size(48, 16);
            this.lb_Email.TabIndex = 5;
            this.lb_Email.Text = "E-Mail:";
            // 
            // tb_Email
            // 
            this.tb_Email.Location = new System.Drawing.Point(173, 144);
            this.tb_Email.Name = "tb_Email";
            this.tb_Email.Size = new System.Drawing.Size(100, 22);
            this.tb_Email.TabIndex = 6;
            // 
            // lib_Datensaetze
            // 
            this.lib_Datensaetze.FormattingEnabled = true;
            this.lib_Datensaetze.ItemHeight = 16;
            this.lib_Datensaetze.Location = new System.Drawing.Point(628, 104);
            this.lib_Datensaetze.Name = "lib_Datensaetze";
            this.lib_Datensaetze.Size = new System.Drawing.Size(442, 148);
            this.lib_Datensaetze.TabIndex = 7;
            // 
            // tb_Suchen
            // 
            this.tb_Suchen.Location = new System.Drawing.Point(479, 107);
            this.tb_Suchen.Name = "tb_Suchen";
            this.tb_Suchen.Size = new System.Drawing.Size(100, 22);
            this.tb_Suchen.TabIndex = 8;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(404, 63);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(55, 16);
            this.label1.TabIndex = 9;
            this.label1.Text = "Suchen:";
            // 
            // lb_Namesuchen
            // 
            this.lb_Namesuchen.AutoSize = true;
            this.lb_Namesuchen.Location = new System.Drawing.Point(404, 107);
            this.lb_Namesuchen.Name = "lb_Namesuchen";
            this.lb_Namesuchen.Size = new System.Drawing.Size(47, 16);
            this.lb_Namesuchen.TabIndex = 10;
            this.lb_Namesuchen.Text = "Name:";
            // 
            // bn_Suchen
            // 
            this.bn_Suchen.Location = new System.Drawing.Point(486, 224);
            this.bn_Suchen.Name = "bn_Suchen";
            this.bn_Suchen.Size = new System.Drawing.Size(93, 30);
            this.bn_Suchen.TabIndex = 11;
            this.bn_Suchen.Text = "Suchen";
            this.bn_Suchen.UseVisualStyleBackColor = true;
            this.bn_Suchen.Click += new System.EventHandler(this.bn_Suchen_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1082, 467);
            this.Controls.Add(this.bn_Suchen);
            this.Controls.Add(this.lb_Namesuchen);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.tb_Suchen);
            this.Controls.Add(this.lib_Datensaetze);
            this.Controls.Add(this.tb_Email);
            this.Controls.Add(this.lb_Email);
            this.Controls.Add(this.bn_Speichern);
            this.Controls.Add(this.tb_Vorname);
            this.Controls.Add(this.lb_Vorname);
            this.Controls.Add(this.lb_Name);
            this.Controls.Add(this.tb_Name);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox tb_Name;
        private System.Windows.Forms.Label lb_Name;
        private System.Windows.Forms.Label lb_Vorname;
        private System.Windows.Forms.TextBox tb_Vorname;
        private System.Windows.Forms.Button bn_Speichern;
        private System.Windows.Forms.Label lb_Email;
        private System.Windows.Forms.TextBox tb_Email;
        private System.Windows.Forms.ListBox lib_Datensaetze;
        private System.Windows.Forms.TextBox tb_Suchen;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label lb_Namesuchen;
        private System.Windows.Forms.Button bn_Suchen;
    }
}

