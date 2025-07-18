using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wkffl.SalaryGen.Parsers;

namespace Wkffl.SalaryGen.Players
{
    internal enum RankingsType
    {
        Ppr,
        Hppr,
        Std,
        PositionSpecific,
    }

    internal static class RankingsLoaderExtensions
    {
        public static IEnumerable<RankingsHandler> GetRankingsHandlers(this RankingsType rankingsType, string year)
        {
            List<RankingsHandler> handlers = new List<RankingsHandler>();

            switch (rankingsType)
            {
                case RankingsType.PositionSpecific:
                    IEnumerable<string> files = Directory.EnumerateFiles($".\\Adp\\{year}\\positions");
                    foreach(string file in files)
                    {
                        StreamReader fileReader = File.OpenText(file);
                        string position = file.Split('.', '\\')[^2];
                        handlers.Add(new RankingsHandler(fileReader, new FantasyProsPositionSpecificAdpParser(position)));
                    }
                    break;

                default:
                    StreamReader streamReader = File.OpenText($".\\Adp\\{year}\\{rankingsType}.csv");
                    IRankingsParser parser = new FantasyProsOverallAdpParser();
                    handlers.Add(new RankingsHandler(streamReader, parser));
                    break;
            }

            return handlers;
        }
    }
}
