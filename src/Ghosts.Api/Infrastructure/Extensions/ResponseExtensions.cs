// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Microsoft.AspNetCore.Http;

namespace Ghosts.Api.Infrastructure.Extensions
{
    public static class ResponseExtensions
    {
        public static void AddApplicationError(this HttpResponse response, string message)
        {
            response.Headers.Append("Application-Error", message);
            // CORS
            response.Headers.Append("access-control-expose-headers", "Application-Error");
        }
    }
}
