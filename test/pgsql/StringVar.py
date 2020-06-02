"""Module for testing string variables."""

class TestStringVar(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.rawData = [
                (1, 'String 1', None),
                (2, 'String 2B', 'Nullable One'),
                (3, 'String 3XX', None),
                (4, 'String 4YYY', 'Nullable Two')
        ]
        self.dataByKey = {}
        for dataTuple in self.rawData:
            key = dataTuple[0]
            self.dataByKey[key] = dataTuple

    def testBindString(self):
        "test binding in a string"
        self.cursor.execute("""
                select * from TestStrings
                where StringCol = ?""",
                "String 3XX")
        self.failUnlessEqual(self.cursor.fetchall(), [self.dataByKey[3]])

    def testBindStringAfterNumber(self):
        "test binding in a string after setting input sizes to a number"
        self.cursor.setinputsizes(ceODBC.NUMBER)
        self.cursor.execute("""
                select * from TestStrings
                where StringCol = ?""",
                "String 2B")
        self.failUnlessEqual(self.cursor.fetchall(), [self.dataByKey[2]])

    def testBindNull(self):
        "test binding in a null"
        self.cursor.execute("""
                select * from TestStrings
                where StringCol = ?""",
                None)
        self.failUnlessEqual(self.cursor.fetchall(), [])

    def testBindLongStringAfterSettingSize(self):
        "test that setinputsizes() returns a long variable"
        var = self.cursor.setinputsizes(90000)[0]
        self.failUnlessEqual(var.type, ceODBC.STRING)
        inString = "1234567890" * 9000
        var.setvalue(0, inString)
        outString = var.getvalue()
        self.failUnlessEqual(inString, outString,
                "output does not match: in was %d, out was %d" % \
                (len(inString), len(outString)))

    def testCursorDescription(self):
        "test cursor description is accurate"
        self.cursor.execute("select * from TestStrings")
        self.failUnlessEqual(self.cursor.description,
                [ ('intcol', ceODBC.NUMBER, 11, 10, 10, 0, False),
                  ('stringcol', ceODBC.STRING, 20, 20, 0, 0, False),
                  ('nullablecol', ceODBC.STRING, 50, 50, 0, 0, True) ])

    def testFetchAll(self):
        "test that fetching all of the data returns the correct results"
        self.cursor.execute("select * From TestStrings order by IntCol")
        self.failUnlessEqual(self.cursor.fetchall(), self.rawData)
        self.failUnlessEqual(self.cursor.fetchall(), [])

    def testFetchMany(self):
        "test that fetching data in chunks returns the correct results"
        self.cursor.execute("select * From TestStrings order by IntCol")
        self.failUnlessEqual(self.cursor.fetchmany(2), self.rawData[0:2])
        self.failUnlessEqual(self.cursor.fetchmany(1), self.rawData[2:3])
        self.failUnlessEqual(self.cursor.fetchmany(4), self.rawData[3:])
        self.failUnlessEqual(self.cursor.fetchmany(3), [])

    def testFetchOne(self):
        "test that fetching a single row returns the correct results"
        self.cursor.execute("""
                select *
                from TestStrings
                where IntCol in (3, 4)
                order by IntCol""")
        self.failUnlessEqual(self.cursor.fetchone(), self.dataByKey[3])
        self.failUnlessEqual(self.cursor.fetchone(), self.dataByKey[4])
        self.failUnlessEqual(self.cursor.fetchone(), None)

    def testSupplementalCharacters(self):
        "test binding and fetching supplemental characters"
        supplementalChars = "𠜎 𠜱 𠝹 𠱓 𠱸 𠲖 𠳏 𠳕 𠴕 𠵼 𠵿 𠸎 𠸏 𠹷 𠺝 " \
                "𠺢 𠻗 𠻹 𠻺 𠼭 𠼮 𠽌 𠾴 𠾼 𠿪 𡁜 𡁯 𡁵 𡁶 𡁻 𡃁 𡃉 𡇙 𢃇 " \
                "𢞵 𢫕 𢭃 𢯊 𢱑 𢱕 𢳂 𢴈 𢵌 𢵧 𢺳 𣲷 𤓓 𤶸 𤷪 𥄫 𦉘 𦟌 𦧲 " \
                "𦧺 𧨾 𨅝 𨈇 𨋢 𨳊 𨳍 𨳒 𩶘"
        self.cursor.execute("truncate table TestTempTable")
        self.cursor.execute("""
                insert into TestTempTable (IntCol, StringCol)
                values (?, ?)""",
                (1, supplementalChars))
        self.connection.commit()
        self.cursor.execute("select StringCol from TestTempTable")
        value, = self.cursor.fetchone()
        self.assertEqual(value, supplementalChars)
