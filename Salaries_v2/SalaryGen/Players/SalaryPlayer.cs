using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wkffl.SalaryGen.Players
{
    internal class SalaryPlayer
    {
        public readonly RankingPlayer Player;
        public readonly double Salary;

        public SalaryPlayer(RankingPlayer player, double salary)
        {
            this.Player = player;
            this.Salary = salary;
        }
    }
}
