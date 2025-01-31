// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

namespace Ghosts.Domain.Code.Helpers
{
    public static class NumberExtensions
    {
        public static bool IsDivisibleByN(this double n, int divisibleBy)
        {
            return n % divisibleBy == 0;
        }

        public static bool IsDivisibleByN(this int n, int divisibleBy)
        {
            return n % divisibleBy == 0;
        }
    }
}
