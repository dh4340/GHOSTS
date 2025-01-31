// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Linq;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;

namespace Ghosts.Api.Infrastructure.Filters;

public class CustomDocumentFilter : IDocumentFilter
{
    public void Apply(OpenApiDocument swaggerDoc, DocumentFilterContext context)
    {
        foreach (var path in swaggerDoc.Paths)
        {
            foreach (var operation in path.Value.Operations)
            {
                var actionDescriptor = context.ApiDescriptions
                    .FirstOrDefault(desc => desc.RelativePath == path.Key.Substring(1))
                    ?.ActionDescriptor;

                if (actionDescriptor != null && actionDescriptor.RouteValues.TryGetValue("action", out var value))
                {
                    operation.Value.OperationId = value;
                }
            }
        }
    }
}
