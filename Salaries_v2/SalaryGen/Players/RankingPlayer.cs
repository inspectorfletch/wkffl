using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace Wkffl.SalaryGen.Players
{
    internal class RankingPlayer
    {
        private readonly Dictionary<RankingsType, int> _overallRankings = new Dictionary<RankingsType, int>();
        private readonly Dictionary<RankingsType, int> _positionRankings = new Dictionary<RankingsType, int>();
        private readonly Dictionary<RankingsType, double> _avgRankings = new Dictionary<RankingsType, double>();

        public readonly string Name;
        public readonly string Position;
        public readonly string Team;

        public string Identifier { get { return $"{this.Position} {this.Name.ToUpper()} ({this.Team})"; } }

        public double OverallRanking { get { return this._overallRankings.Values.Average(); } }
        public double PositionRanking { get { return this._positionRankings.Values.Average(); } }
        public double AvgRanking { get { return this._avgRankings.Values.Average(); } }

        public RankingPlayer(string name, string position, string team)
        {
            this.Name = name;
            this.Position = position;
            this.Team = team;
        }

        public void AddRanking(RankingsType type, int overallRanking, int positionRanking, double avgRanking)
        {
            this._overallRankings.Add(type, overallRanking);
            this._positionRankings.Add(type, positionRanking);
            this._avgRankings.Add(type, avgRanking);
        }

        public override string ToString()
        {
            return $"{this.Position} {this.Name} ({this.Team}): {this.OverallRanking} overall, {this.Position}{this.PositionRanking} ({this.AvgRanking})";
        }
    }
}
