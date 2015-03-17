namespace QuizBotPlugin.Forms
{
    partial class QuizBuilder
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.loadQuizFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.saveQuizFileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.quitItems = new System.Windows.Forms.ListBox();
            this.delItem = new System.Windows.Forms.Button();
            this.newItem = new System.Windows.Forms.Button();
            this.saveQuiz = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.quizID = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.quizQuestion = new System.Windows.Forms.TextBox();
            this.quizAnwser = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(573, 24);
            this.menuStrip1.TabIndex = 0;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.loadQuizFileToolStripMenuItem,
            this.saveQuizFileToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // loadQuizFileToolStripMenuItem
            // 
            this.loadQuizFileToolStripMenuItem.Name = "loadQuizFileToolStripMenuItem";
            this.loadQuizFileToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.loadQuizFileToolStripMenuItem.Text = "Load Quiz File";
            this.loadQuizFileToolStripMenuItem.Click += new System.EventHandler(this.loadQuizFileToolStripMenuItem_Click);
            // 
            // saveQuizFileToolStripMenuItem
            // 
            this.saveQuizFileToolStripMenuItem.Name = "saveQuizFileToolStripMenuItem";
            this.saveQuizFileToolStripMenuItem.Size = new System.Drawing.Size(152, 22);
            this.saveQuizFileToolStripMenuItem.Text = "Save Quiz File";
            this.saveQuizFileToolStripMenuItem.Click += new System.EventHandler(this.saveQuizFileToolStripMenuItem_Click);
            // 
            // quitItems
            // 
            this.quitItems.FormattingEnabled = true;
            this.quitItems.Location = new System.Drawing.Point(0, 27);
            this.quitItems.Name = "quitItems";
            this.quitItems.Size = new System.Drawing.Size(230, 303);
            this.quitItems.TabIndex = 1;
            this.quitItems.SelectedIndexChanged += new System.EventHandler(this.quitItems_SelectedIndexChanged);
            // 
            // delItem
            // 
            this.delItem.Location = new System.Drawing.Point(0, 336);
            this.delItem.Name = "delItem";
            this.delItem.Size = new System.Drawing.Size(75, 23);
            this.delItem.TabIndex = 2;
            this.delItem.Text = "Delete Item";
            this.delItem.UseVisualStyleBackColor = true;
            this.delItem.Click += new System.EventHandler(this.delItem_Click);
            // 
            // newItem
            // 
            this.newItem.Location = new System.Drawing.Point(155, 336);
            this.newItem.Name = "newItem";
            this.newItem.Size = new System.Drawing.Size(75, 23);
            this.newItem.TabIndex = 3;
            this.newItem.Text = "New Item";
            this.newItem.UseVisualStyleBackColor = true;
            this.newItem.Click += new System.EventHandler(this.newItem_Click);
            // 
            // saveQuiz
            // 
            this.saveQuiz.Location = new System.Drawing.Point(438, 336);
            this.saveQuiz.Name = "saveQuiz";
            this.saveQuiz.Size = new System.Drawing.Size(135, 23);
            this.saveQuiz.TabIndex = 4;
            this.saveQuiz.Text = "Save Quiz";
            this.saveQuiz.UseVisualStyleBackColor = true;
            this.saveQuiz.Click += new System.EventHandler(this.saveQuiz_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(245, 39);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(45, 13);
            this.label1.TabIndex = 5;
            this.label1.Text = "Quiz ID:";
            // 
            // quizID
            // 
            this.quizID.Location = new System.Drawing.Point(296, 36);
            this.quizID.Name = "quizID";
            this.quizID.ReadOnly = true;
            this.quizID.Size = new System.Drawing.Size(277, 20);
            this.quizID.TabIndex = 6;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(238, 90);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(52, 13);
            this.label2.TabIndex = 7;
            this.label2.Text = "Question:";
            // 
            // quizQuestion
            // 
            this.quizQuestion.Location = new System.Drawing.Point(296, 87);
            this.quizQuestion.Name = "quizQuestion";
            this.quizQuestion.Size = new System.Drawing.Size(277, 20);
            this.quizQuestion.TabIndex = 8;
            // 
            // quizAnwser
            // 
            this.quizAnwser.Location = new System.Drawing.Point(296, 137);
            this.quizAnwser.Name = "quizAnwser";
            this.quizAnwser.Size = new System.Drawing.Size(277, 20);
            this.quizAnwser.TabIndex = 10;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(243, 140);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(45, 13);
            this.label3.TabIndex = 9;
            this.label3.Text = "Anwser:";
            // 
            // QuizBuilder
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(573, 360);
            this.Controls.Add(this.quizAnwser);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.quizQuestion);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.quizID);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.saveQuiz);
            this.Controls.Add(this.newItem);
            this.Controls.Add(this.delItem);
            this.Controls.Add(this.quitItems);
            this.Controls.Add(this.menuStrip1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MainMenuStrip = this.menuStrip1;
            this.MaximizeBox = false;
            this.Name = "QuizBuilder";
            this.Text = "QuizBuilder";
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem loadQuizFileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem saveQuizFileToolStripMenuItem;
        private System.Windows.Forms.ListBox quitItems;
        private System.Windows.Forms.Button delItem;
        private System.Windows.Forms.Button newItem;
        private System.Windows.Forms.Button saveQuiz;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox quizID;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox quizQuestion;
        private System.Windows.Forms.TextBox quizAnwser;
        private System.Windows.Forms.Label label3;
    }
}