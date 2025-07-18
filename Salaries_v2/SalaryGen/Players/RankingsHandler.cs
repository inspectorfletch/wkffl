using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Wkffl.SalaryGen.Parsers;

namespace Wkffl.SalaryGen.Players
{
    internal class RankingsHandler
    {
        public readonly StreamReader FileStream;
        public readonly IRankingsParser Parser;

        public RankingsHandler(StreamReader fileStream, IRankingsParser parser)
        {
            this.FileStream = fileStream;
            this.Parser = parser;
        }
    }
}
