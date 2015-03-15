using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Timers;
using QuizBotPlugin.ListItems;
using Spiff.Core;
using Spiff.Core.API.Commands;
using Spiff.Core.API.EventArgs;
using Spiff.Core.Utils;

namespace QuizBotPlugin
{
    public class QuizMaster
    {
        private readonly string _file;
        private readonly Command _comm;
        private List<QuizItem> _quizItems;
        private QuizItem _currentItem;
        private Timer Timer;
        private int _id = 0;
        private bool NoPost = false;

        public QuizMaster(string file)
        {
            _file = file;


            _quizItems =
                Utils.DeserializeFromXml<List<QuizItem>>(
                    File.ReadAllText(Path.Combine(QuizBot.BotInstance.PluginDirectory, file)));

            Timer = new Timer {Interval = 60000};
            Timer.Elapsed += TimerOnTick;

            _currentItem = getQuizItem();

            TwitchIRC.Instance.OnChatHandler += InstanceOnOnChatHandler;

            Timer.Start();
        }

        private void InstanceOnOnChatHandler(object sender, OnChatEvent onChatEvent)
        {
            //Logger.Debug("Fired Message Event:" + onChatEvent.Message, QuizBot.BotInstance.Name);
            if (onChatEvent.Message.Trim().Equals(_currentItem.Anwser))
            {
                //NoPost = true;
                Timer.Stop();
                //NoPost = false;
                TwitchIRC.Instance.WriteOut.SendMessage(onChatEvent.User + " got the anwser correct!");
                _currentItem = getQuizItem();
                if(Timer != null)
                    Timer.Start();
            }
        }

        private void TimerOnTick(object sender, EventArgs eventArgs)
        {
            if (_currentItem == null)
            {
                Logger.Error("Current Quiz item seems to be null", QuizBot.BotInstance.Name);
                return;
            }
            //if (NoPost) return;
            TwitchIRC.Instance.WriteOut.SendMessage("The anwser for the question was: " + _currentItem.Anwser);
            _currentItem = getQuizItem();
            if(Timer != null)
                Timer.Start();
        }

        private QuizItem getQuizItem()
        {
            if (_id > _quizItems.Count - 1)
            {
                _id = 0;
                TwitchIRC.Instance.OnChatHandler -= InstanceOnOnChatHandler;
                TwitchIRC.Instance.WriteOut.SendMessage("Game Over... Maybe I will load another :D");
                Timer.Elapsed -= TimerOnTick;
                Timer.Dispose();
                Timer = null;
                return null;
            }
            var item = _quizItems[_id];
            _id++;

            TwitchIRC.Instance.WriteOut.SendMessage(item.Question);
            return item;
        }
    }
}
