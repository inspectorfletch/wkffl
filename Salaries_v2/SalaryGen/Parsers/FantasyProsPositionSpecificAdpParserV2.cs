using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Wkffl.SalaryGen.Players;

namespace Wkffl.SalaryGen.Parsers
{
    class FantasyProsPositionSpecificAdpParserV2 : IRankingsParser
    {
        private readonly string _position;

        public FantasyProsPositionSpecificAdpParserV2(string position)
        {
            this._position = position;
        }

        public ParsedPlayer ParsePlayerLine(string[] splitLine)
        {
            int positionRanking = int.Parse(splitLine[0].Trim('"'));

            string rawOverallRanking = splitLine[0].Trim('"');
            int overallRanking = int.Parse(rawOverallRanking);

            string nameAndTeam = splitLine[2].Trim('"');
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
                name = string.Join(' ', new ArraySegment<string>(nameAndTeamParts, 0, nameAndTeamParts.Length - 2));
                team = nameAndTeamParts[^2];
            }

            if (string.IsNullOrWhiteSpace(team))
            {
                team = "FA";
            }

            double avgRanking = double.Parse(splitLine[^1].Trim('"'));

            RankingPlayer playerDescriptor = new RankingPlayer(name, this._position, team);
            return new ParsedPlayer(playerDescriptor, overallRanking, positionRanking, avgRanking);
        }
    }
}
