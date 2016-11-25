#=============================================================================
#
# depends Module Unit Tests
#
#=============================================================================

"""
depends Module Unit Tests
=========================
"""


import unittest

import fab


__version__ = '0.0.0'


#=============================================================================
class DependsTests( unittest.TestCase ):
    """
    Tests the depends module.
    """


    #=========================================================================
    def setUp( self ):
        """
        Performs test setup.
        """
        fab.depends._conf[ 'paths' ] = []
        fab.depends._conf[ 'rules' ] = []


    #=========================================================================
    def test_global_path_adding( self ):
        """
        Tests addition of paths to global configuration.
        """

        before = list( fab.depends._conf[ 'paths' ] )
        fab.depends.setup( paths = [ 'testpath' ] )
        after = fab.depends._conf[ 'paths' ]

        self.assertListEqual( before, [] )
        self.assertListEqual( after, [ 'testpath' ] )


    #=========================================================================
    def test_scanner_path_adding( self ):
        """
        Tests addition of paths to scanner configuration.
        """

        scanner = fab.depends.scanner( 'test.txt' )

        before = list( scanner._conf[ 'paths' ] )
        scanner.setup( paths = [ 'testpath' ] )
        after = scanner._conf[ 'paths' ]

        self.assertListEqual( before, [ '' ] )
        self.assertListEqual( after, [ '', 'testpath' ] )


    #=========================================================================
    def test_rule_adding( self ):
        """
        Tests addition of rules to global configuration.
        """

        class TestRule( fab.depends.Rule ):
            pass

        before = list( fab.depends._conf[ 'rules' ] )
        fab.depends.addrule( TestRule )
        after = fab.depends._conf[ 'rules' ]

        self.assertListEqual( before, [] )
        self.assertListEqual( after, [ TestRule ] )

