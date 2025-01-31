// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Linq;
using Ghosts.Api.Infrastructure.Data;
using Microsoft.AspNetCore.Mvc;

namespace ghosts.api.Controllers;

[Controller]
[Produces("application/json")]
[Route("view-activities")]
[ApiExplorerSettings(IgnoreApi = true)]
public class ViewActivitiesController(ApplicationDbContext context) : Controller
{
    private readonly ApplicationDbContext _context = context;

    [HttpGet]
    public IActionResult Index()
    {
        var list = _context.Npcs.ToList().OrderBy(o => o.Enclave).ThenBy(o => o.Team);
        return View("Index", list);
    }

    [HttpGet("{id:guid}")]
    public IActionResult Detail(Guid id)
    {
        var o = _context.Npcs.FirstOrDefault(x => x.Id == id);
        return View("Detail", o);
    }
}
