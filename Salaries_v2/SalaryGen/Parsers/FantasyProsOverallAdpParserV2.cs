using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Wkffl.SalaryGen.Players;

namespace Wkffl.SalaryGen.Parsers
{
    internal class FantasyProsOverallAdpParserV2 : IRankingsParser
    {
        public ParsedPlayer ParsePlayerLine(string[] splitLine)
        {
            int overallRanking = int.Parse(splitLine[0].Trim('"'));
            string nameAndTeam = splitLine[1].Trim('"');
            string[] nameAndTeamParts = nameAndTeam.Split(' ', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

            string name = null;
            string team = null;
            if (!nameAndTeamParts[^1].StartsWith('('))
            {
                name = nameAndTeam.Trim();
                team = "FA";
            }
            else
            {
                name = String.Join(' ', new ArraySegment<string>(nameAndTeamParts, 0, nameAndTeamParts.Length - 2));
                team = nameAndTeamParts[^2];
            }

            string posAndRanking = splitLine[2];
            string position = Regex.Match(posAndRanking, @"([A-Z]+)").Value;

            int positionRanking = int.Parse(Regex.Match(posAndRanking, @"\d+").Value);

            double avgRanking = double.Parse(splitLine[^1].Trim('"'));

            RankingPlayer playerDescriptor = new RankingPlayer(name, position, team);
            return new ParsedPlayer(playerDescriptor, overallRanking, positionRanking, avgRanking);
        }
    }
}
