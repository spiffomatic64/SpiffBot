using System.ComponentModel;
using System.Linq;

namespace Spiff.Core.Extensions
{
    public static class StringExtensions
    {
        public static bool IsAllUpper(this string @string)
        {
            return @string.All(char.IsUpper);
        }

        public static bool IsAllLower(this string @string)
        {
            return @string.All(char.IsLower);
        }

        public static bool IsNumbers(this string @string)
        {
            return @string.All(char.IsDigit);
        }

        public static T Parse<T>(this string value)
        {
            // Get default value for type so if string
            // is empty then we can return default value.
            T result = default(T);
            if (!string.IsNullOrEmpty(value))
            {
                // we are not going to handle exception here
                // if you need SafeParse then you should create
                // another method specially for that.
                TypeConverter tc = TypeDescriptor.GetConverter(typeof(T));
                result = (T)tc.ConvertFrom(value);
            } return result;
        }

        public static string Truncate(this string text, int maxLength)
        {
            // replaces the truncated string to a ...
            const string suffix = "...";
            string truncatedString = text;

            if (maxLength <= 0) return truncatedString;
            int strLength = maxLength - suffix.Length;

            if (strLength <= 0) return truncatedString;

            if (text == null || text.Length <= maxLength) return truncatedString;

            truncatedString = text.Substring(0, strLength);
            truncatedString = truncatedString.TrimEnd();
            truncatedString += suffix;
            return truncatedString;
        }
    }
}
