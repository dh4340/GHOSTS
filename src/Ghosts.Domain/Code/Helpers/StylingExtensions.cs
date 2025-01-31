// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Drawing;

namespace Ghosts.Domain.Code.Helpers
{
    public static class StylingExtensions
    {
        public static Color GetRandomColor()
        {
            var random = new Random();
            return Color.FromArgb((byte)random.Next(0, 255), (byte)random.Next(0, 255), (byte)random.Next(0, 255));
        }
    }
}
