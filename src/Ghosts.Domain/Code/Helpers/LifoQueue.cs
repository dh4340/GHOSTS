// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Collections.Generic;

namespace Ghosts.Domain.Code.Helpers
{
    public class LifoQueue<T> : LinkedList<T>
    {
        private readonly int _capacity;

        public LifoQueue(int capacity)
        {
            _capacity = capacity;
        }

        public void Add(T item)
        {
            if (Count > 0 && Count == _capacity) RemoveLast();
            AddFirst(item);
        }
    }
}
