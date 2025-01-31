// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System.IO;
using System.IO.Compression;

namespace ghosts.api.Infrastructure.Extensions;

public static class ZipExtensions
{
    public static void ZipDirectoryContents(this string sourceDirectory, string zipFileOutputPath)
    {
        if (string.IsNullOrEmpty(zipFileOutputPath)) return;
        if (File.Exists(zipFileOutputPath))
            File.Delete(zipFileOutputPath);

        using var zip = ZipFile.Open(zipFileOutputPath, ZipArchiveMode.Create);
        var files = Directory.GetFiles(sourceDirectory);
        foreach (var file in files)
        {
            var relativePath = Path.GetRelativePath(sourceDirectory, file);
            zip.CreateEntryFromFile(file, relativePath, CompressionLevel.SmallestSize);
        }
    }
}
