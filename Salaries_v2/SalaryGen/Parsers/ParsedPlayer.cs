using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wkffl.SalaryGen.Players;

namespace Wkffl.SalaryGen.Parsers
{
    internal class ParsedPlayer
    {
        public RankingPlayer Player { get; private set; }
        public readonly int OverallRanking;
        public readonly int PositionRanking;
        public readonly double AvgRanking;

        public ParsedPlayer(RankingPlayer player, int overallRanking, int positionRanking, double avgRanking)
        {
            this.Player = player;
            this.OverallRanking = overallRanking;
            this.PositionRanking = positionRanking;
            this.AvgRanking = avgRanking;
        }
    }
}
