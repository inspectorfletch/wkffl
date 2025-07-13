using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Wkffl.SalaryGen.Players;

namespace Wkffl.SalaryGen.Parsers
{
    internal class FantasyProsAdpParser : IRankingsParser
    {
        public ParsedPlayer ParsePlayerLine(string[] splitLine)
        {
            int overallRanking = int.Parse(splitLine[0].Trim('"'));
            string name = splitLine[1].Trim('"');
            string team = splitLine[2].Trim('"').ToUpper();

            if (string.IsNullOrWhiteSpace(team))
            {
                team = "FA";
            }

            string posAndRanking = splitLine[4];
            string position = Regex.Match(posAndRanking, @"([A-Z]+)").Value;

            int positionRanking = int.Parse(Regex.Match(posAndRanking, @"\d+").Value);

            double avgRanking = double.Parse(splitLine[^1].Trim('"'));

            RankingPlayer playerDescriptor = new RankingPlayer(name, position, team);
            return new ParsedPlayer(playerDescriptor, overallRanking, positionRanking, avgRanking);
        }
    }
}
