using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Wkffl.SalaryGen.Players;

namespace Wkffl.SalaryGen.Parsers
{
    class FantasyProsPositionSpecificAdpParser : IRankingsParser
    {
        private readonly string _position;

        public FantasyProsPositionSpecificAdpParser(string position)
        {
            this._position = position;
        }

        public ParsedPlayer ParsePlayerLine(string[] splitLine)
        {
            int positionRanking = int.Parse(splitLine[0].Trim('"'));

            int overallRanking = int.MaxValue;
            string rawOverallRanking = splitLine[1].Trim('"');
            int.TryParse(rawOverallRanking, out overallRanking);

            string name = splitLine[2].Trim('"');
            string team = splitLine[3].Trim('"').ToUpper();

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
