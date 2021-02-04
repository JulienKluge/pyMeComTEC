//#define IS_RELEASED 

using System.Reflection;
#if (IS_RELEASED)
[assembly: AssemblyVersion(VersionDefinition.Major + "." + VersionDefinition.Minor + ".2.103")]
[assembly: AssemblyInformationalVersion(VersionDefinition.Major + "." + VersionDefinition.Minor + ".2.103  Rev. 18c68217 Released")]
#else
[assembly: AssemblyVersion(VersionDefinition.Major + "." + VersionDefinition.Minor + ".1.103")]
[assembly: AssemblyInformationalVersion(VersionDefinition.Major + "." + VersionDefinition.Minor + ".1.103  Rev. 18c68217 Committed")]
#endif



/// <summary>Defines the version of the assembly.</summary>
static internal class VersionDefinition
{
    /// <summary>Big version before the dot.</summary>
    public const string Major = "1";
    /// <summary>Small version behind the dot.</summary>
    public const string Minor = "47";
}
