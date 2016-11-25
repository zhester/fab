#=============================================================================
#
# Dependency Discovery Tool
#
#=============================================================================

"""
Dependency Discovery Tool
=========================

Allows programs to determine dependency chains based on project-specific
rules.  Most commonly, dependency relationships are useful for software build
systems, but can also be used for content management, testing, or other
automated production systems.

Usage Examples
--------------

import depends

# Global configuration interface.
depends.setup( paths = [ 'includes' ] )

# Create a dependency scanner.
# Note: Directory of a source file is always scanned.
# Note: The scanning type and rules are usually detected automatically.
scanner = depends.scanner( 'path/to/sourcefile.c' )

# Local configuration interface.
scanner.setup( paths = [ 'path/to/includes' ] )

# Iterator supported to retrieve all dependencies.
# Note: Each dependency contains complete path information.
for dep in scanner:
    print( 'Dependency:', dep )


#=============================================================================
class MyRule( Rule ):
    '''
    Example of a customized dependency scanning and detection rule.
    '''

    # File extensions used to determine what files should match this rule.
    extensions = ( 'ext1', 'ext2' )

    # Patterns used to determine dependencies based on file content.
    extracts = ( r'!import\s+['"]([^'"]+)['"]', )

    # Patterns used to determine what files should match this rule.
    names = ( r'special_\S+\.ext$', )

    #=========================================================================
    def check_source( self, path, match = None ):
        '''
        Called each time a matching source file is found.
        Note: If the `extracts` property can comprehensively determine
        dependencies for a rule, this method does not need to be defined.

        @param path  The complete path to the matched source file
        @param match A possible match object from file name matching
        @return      An iterable object that enumerates all dependencies
        '''
        return ()

# Add the custom rule to the dependency scanning system.
depends.addrule( MyRule )

"""


import os
import re


__version__ = '0.0.0'


#=============================================================================
class Rule( object ):
    """
    Models a dependency rule.
    """

    # Patterns used to determine what files should match this rule.
    names = ()

    # File extensions used to determine what files should match this rule.
    extensions = ()

    # Patterns used to determine dependencies based on file content.
    extracts = ()


    #=========================================================================
    def __init__( self ):
        """
        Initializes a Rule object.
        """

        # The result of the most recent name pattern match test.
        self.match = None


    #=========================================================================
    def check_source( self, path, match = None ):
        """
        Called each time a matching source file is found.
        Note: If the `extracts` property can comprehensively determine
        dependencies for a rule, this method does not need to be defined.

        @param path  The complete path to the matched source file
        @param match A possible match object from file name matching
        @return      An iterable object that enumerates all dependencies
        """
        ### ZIH
        raise NotImplementedError()


    #=========================================================================
    def match_name( self, path ):
        """
        Tests a file name to see if it matches this rule.

        @param path A complete path to the file name to test
        @return     True for a matching file name
        """

        # Patterns based on file name extensions.
        patterns = [ r'.+\.' + ext + '$' for ext in self.extensions ]

        # Special file name patterns.
        patterns += list( self.names )

        # Scan all patterns against this file name.
        for pattern in patterns:
            match = re.match( pattern, path )
            if match is not None:
                self.match = match
                return True

        # File name did not match any patterns.
        self.match = None
        return False


#=============================================================================
class CRule( object ):
    """
    C code dependency rule.
    """
    extensions = ( 'c', 'h' )
    extracts   = ( r'#include\s*["]([^"]+)["]', )


#=============================================================================
class Scanner( object ):
    """
    Provides an interface for defining dependency scanning techniques.
    """


    #=========================================================================
    def __init__( self, path ):
        """
        Initializes a Scanner object.

        @param path The path to the source file to scan for dependencies
        """

        # Path to file being scanned for dependencies.
        self._path = path

        # Per-scanner configuration starts with global configuration.
        self._conf = dict( _conf )

        # Directory to this file.
        path_dir = os.path.dirname( self._path )

        # Make sure current path is in list.
        if path_dir not in self._conf[ 'paths' ]:
            self._conf[ 'paths' ].insert( 0, path_dir )


    #=========================================================================
    def __iter__( self ):
        """
        Provides iterable object support.

        @return An iterable object that yields all dependencies for the
                current scanning context
        """
        ### ZIH
        raise NotImplementedError()


    #=========================================================================
    def setup( self, **kwargs ):
        """
        Scanner configuration function.

        @param kwargs Keyword arguments specify configuration data
                      paths : List of paths to append to path list
        """
        _setup_dict( self._conf, **kwargs )


#=============================================================================
# Module Variables

# Module-level configuration.
_conf = {
    'paths' : [],
    'rules' : []
}


#=============================================================================
# Module Interface Functions


#=============================================================================
def addrule( rule ):
    """
    Adds a rule to the list of scanning/detection rules.

    @param rule The rule to add to the list of scanning/detection rules
    """
    _setup_dict( _conf, rules = [ rule ] )


#=============================================================================
def scanner( path ):
    """
    Creates a dependency scanning object for a given source file name.

    ZIH
    """

    # Test for an assumed rule list.
    if len( _conf[ 'rules' ] ) == 0:
        _conf[ 'rules' ] = [ CRule ]

    # Create the dependency scanner for the requested file name.
    return Scanner( path )


#=============================================================================
def setup( **kwargs ):
    """
    Module-level configuration function.

    ZIH
    """
    _setup_dict( _conf, **kwargs )


#=============================================================================
# Module Private Functions


#=============================================================================
def _setup_dict( conf, **kwargs ):
    """
    Provides normalized dictionary configuration management.

    @param conf   The target configuration dictionary
    @param kwargs Keyword arguments used to update the configuration
    """

    # Append-mode lists.
    applists = ( 'paths', 'rules' )

    # Existing append-mode lists.
    oldlists = {}

    # Save any lists that need to have items appended to them.
    for alist in applists:
        if alist in kwargs:
            oldlists[ alist ] = conf[ alist ]

    # Update all other config values.
    conf.update( kwargs )

    # Restore the saved lists.
    for alist in oldlists:
        conf[ alist ] = oldlists[ alist ]

        # Append any new entries to the list.
        for newitem in kwargs[ alist ]:
            if newitem not in conf[ alist ]:
                conf[ alist ].append( newitem )

