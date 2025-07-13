using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Wkffl.SalaryGen.Parsers
{
    internal interface IRankingsParser
    {
        ParsedPlayer ParsePlayerLine(string[] splitLine);
    }
}
