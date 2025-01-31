// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Threading.Tasks;
using Microsoft.Extensions.Logging;

namespace Ghosts.Api.Infrastructure.Data
{
    public class DbInitializer
    {
        public static async Task Initialize(ApplicationDbContext context, ILogger<DbInitializer> logger)
        {
            await context.Database.EnsureCreatedAsync();

            // Could do additional seeding here in the future
            //if (context.Machines.Any()) return; // DB has been seeded
        }
    }
}
