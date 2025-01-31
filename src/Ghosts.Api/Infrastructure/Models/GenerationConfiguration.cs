// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections.Generic;
using Swashbuckle.AspNetCore.Filters;

namespace ghosts.api.Infrastructure.Models;

/// <summary>
/// The configuration for generating a large number of NPCs for your scenario
/// </summary>
public class GenerationConfiguration
{
    // A campaign is the top level of an engagement
    public string Campaign { get; set; }
    // Enclaves are specific subnets of a range, (or a larger number of people) 
    public IList<EnclaveConfiguration> Enclaves { get; set; }
}

public class EnclaveConfiguration
{
    public string Name { get; set; }
    public IList<TeamConfiguration> Teams { get; set; }
}

public class TeamConfiguration
{
    public NpcConfiguration Npcs { get; set; }
    public string Name { get; set; }
    public string MachineNameTemplate { get; set; }
    public string DomainTemplate { get; set; }

    public IEnumerable<PreferenceOption> PreferenceSettings { get; set; }
}

/// <summary>
/// NPC generation configuration
/// </summary>
public class NpcConfiguration
{
    /// <summary>
    /// The number of NPCs to generate
    /// </summary>
    public int Number { get; set; }
    /// <summary>
    /// The configuration to tune the generation of NPCs 
    /// </summary>
    public NpcGenerationConfiguration Configuration { get; set; }
}

public class GenerationConfigurationExample : IExamplesProvider<GenerationConfiguration>
{
    public GenerationConfiguration GetExamples()
    {

        return new GenerationConfiguration
        {
            Campaign = $"Exercise Season {DateTime.Now.Year}",
            Enclaves = new List<EnclaveConfiguration>
            {
                new()
                {
                    Name = $"Brigade {Faker.Company.Name()}",
                    Teams = new List<TeamConfiguration>
                    {
                        new()
                        {
                            Name = $"Engineering", DomainTemplate = "eng{machine_number}-brigade.unit.co",
                            MachineNameTemplate = "eng{machine_number}",
                            Npcs = new NpcConfiguration
                            {
                                Number = 10,
                                Configuration = new NpcGenerationConfiguration
                                    {Branch = MilitaryBranch.USARMY, Unit = "", RankDistribution = new List<RankDistribution>()}
                            }
                        }
                    }
                }
            }
        };
    }
}
