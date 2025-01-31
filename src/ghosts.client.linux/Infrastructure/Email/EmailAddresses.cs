// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.Collections.Generic;
using System.IO;

namespace ghosts.client.linux.Infrastructure.Email;

public static class EmailListManager
{
    public static List<string> GetDomainList()
    {
        var fileName = ClientConfigurationResolver.EmailDomain;

        if (!File.Exists(fileName))
        {
            throw new FileNotFoundException("Email list could not be generated");
        }

        var list = JsonConvert.DeserializeObject<List<string>>(File.ReadAllText(fileName));
        return list;
    }

    public static List<string> GetOutsideList()
    {
        var fileName = ClientConfigurationResolver.EmailOutside;

        if (!File.Exists(fileName))
            throw new FileNotFoundException($"Email outside list not found at {fileName}");

        var list = JsonConvert.DeserializeObject<List<string>>(File.ReadAllText(fileName));
        return list;
    }
}
