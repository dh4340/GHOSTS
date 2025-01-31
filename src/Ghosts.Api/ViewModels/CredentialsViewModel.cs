// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using Newtonsoft.Json;

namespace Ghosts.Api.ViewModels
{
    public class CredentialsViewModel
    {
        [JsonProperty("username")]
        [JsonRequired]
        public string UserName { get; set; }

        [JsonProperty("password")]
        [JsonRequired]
        public string Password { get; set; }
    }

    public class CredentialsViewModelValidator
    {
    }
}
