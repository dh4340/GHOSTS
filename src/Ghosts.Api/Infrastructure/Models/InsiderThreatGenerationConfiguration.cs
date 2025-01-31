// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections.Generic;
using Swashbuckle.AspNetCore.Filters;

namespace ghosts.api.Infrastructure.Models;

public class InsiderThreatGenerationConfiguration
{
    // A campaign is the top level of an engagement
    public string Campaign { get; set; }

    // Enclaves are specific subnets of a range, (or a larger number of people) 
    public IList<EnclaveConfiguration> Enclaves { get; set; }
}

public class InsiderThreatGenerationConfigurationExample : IExamplesProvider<InsiderThreatGenerationConfiguration>
{
    public InsiderThreatGenerationConfiguration GetExamples()
    {
        return new InsiderThreatGenerationConfiguration
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
