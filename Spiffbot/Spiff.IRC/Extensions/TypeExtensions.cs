using System;

namespace Spiff.Core.Extensions
{
    public static class TypeExtensions
    {
        public static bool HasAbstract(this Type type, Type @abstract)
        {
            return type.IsSubclassOf(@abstract);
        }
    }
}
