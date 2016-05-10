using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using QuizBotPlugin.ListItems;

namespace QuizBotPlugin.Forms
{
    public partial class QuizBuilder : Form
    {
        private List<QuizItem> _quizItems;
        public QuizBuilder()
        {
            InitializeComponent();
            _quizItems = new List<QuizItem>();
        }

        private void loadQuizFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var ofd = new OpenFileDialog
            {
                InitialDirectory = QuizBot.BotInstance.PluginDirectory,
                Title = "Load Quiz",
                Filter = "Quiz File(*.xml)|*.xml"
            };

            var result = ofd.ShowDialog();

            if (result == DialogResult.OK)
            {
                _quizItems = Utils.DeserializeFromXml<List<QuizItem>>(File.ReadAllText(ofd.FileName));

                LoadQuitItems();
            }
        }

        private void saveQuizFileToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var ofd = new SaveFileDialog
            {
                InitialDirectory = QuizBot.BotInstance.PluginDirectory,
                Title = "Save Quiz",
                Filter = "Quiz File(*.xml)|*.xml"
            };

            var result = ofd.ShowDialog();

            if (result == DialogResult.OK)
            {
                Utils.SerializeToXml(_quizItems, ofd.FileName);

                MessageBox.Show("Saved the quiz to: " + ofd.FileName);
                //_quizItems = Utils.DeserializeFromXml<List<QuizItem>>(File.ReadAllText(ofd.FileName));
            }
        }

        private void LoadQuitItems()
        {
           quitItems.Items.Clear();

            foreach (var item in _quizItems)
            {
                quitItems.Items.Add(item.Question);
            }
        }

        private void saveQuiz_Click(object sender, EventArgs e)
        {
            if (quitItems.SelectedIndex <= -1)
            {
                var id = _quizItems.Count;

                _quizItems.Add(new QuizItem(id, quizQuestion.Text, quizAnwser.Text));

                quitItems.Items.Add(quizQuestion.Text);
            }
            else
            {
                var item = (from s in _quizItems where s.ID == quitItems.SelectedIndex select s).FirstOrDefault();
                if (item != null)
                {
                    item.Question = quizQuestion.Text;
                    item.Anwser = quizAnwser.Text;
                }

                LoadQuitItems();
            }
        }

        private void quitItems_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (quitItems.SelectedIndex > -1)
            {
                var item = (from s in _quizItems where s.ID == quitItems.SelectedIndex select s).FirstOrDefault();

                if (item != null)
                {
                    quizID.Text = item.ID.ToString();
                    quizQuestion.Text = item.Question;
                    quizAnwser.Text = item.Anwser;
                }
            }
        }

        private void newItem_Click(object sender, EventArgs e)
        {
            quitItems.ClearSelected();

            quizID.Text = _quizItems.Count.ToString();
        }

        private void delItem_Click(object sender, EventArgs e)
        {
            if (quitItems.SelectedIndex > -1)
            {
                var item = (from s in _quizItems where s.ID == quitItems.SelectedIndex select s).FirstOrDefault();

                if (item != null)
                {
                    _quizItems.Remove(item);
                }
            }
        }
    }
}
