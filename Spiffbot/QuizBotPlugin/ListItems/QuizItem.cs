using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace QuizBotPlugin.ListItems
{
    public class QuizItem
    {
        public int ID { get; set; }
        public string Question { get; set; }
        public string Anwser { get; set; }

        //Cause of how XML works in C#
        public QuizItem() { }

        public QuizItem(int id, string question, string anwser)
        {
            ID = id;
            Question = question;
            Anwser = anwser;
        }
    }
}
