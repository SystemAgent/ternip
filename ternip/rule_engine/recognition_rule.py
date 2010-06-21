#!/usr/bin/env python

import re
from ternip.timex import timex

class recognition_rule:
    """ A class that represents identification rules """
    
    def __init__(self, match,
                       type,
                       guards  = [],
                       id      = None,
                       after   = None,
                       squelch = False):
        """
        Create a recognition rule, with a number of optional arguments. All
        regex's are in the form to be used with nltk.TokenSearcher.findall
        (http://nltk.googlecode.com/svn/trunk/doc/api/nltk.text.TokenSearcher-class.html#findall)
        however with the amendment that the body of the tokens are actually in
        the form <token~POS>, e.g., <about~.+> would match about with any POS
        tag.
        
        id is an optional value which can be used with other rules to express an
            ordering.
        type can be date, time or duration (TIMEX3 annotation guidelines). This
            is a compulsory value.
        match is a regex. The text that is matched by this regex is annotated as
            a timex. Compulsory.
        guard is a list of regexes which must be satisfied for this rule to be
            applied. Defauts to an empty list. If the first character in the
            regex is a !, then it means that it's a negative guard - the guard
            must NOT match for this rule to be applied.
        squelch is a Boolean. If true, then if the 'match' regex matches some
            stuff that's already been timex annotated, those timexes are removed
            and no timex is added to the match. Defaults to false.
        after is a string giving an ID 
        """
        
        # This code is modified from NLTK's text.py for dealing with pattern
        # matching with tokenised strings, under the Apache License 2.0
        
        # Natural Language Toolkit (NLTK) http://www.nltk.org/
        # Copyright (C) 2001-2010 NLTK Project
        # Bird, Steven, Edward Loper and Ewan Klein (2009).
        # Natural Language Processing with Python.  O'Reilly Media Inc.
        
        match = re.sub(r'\s', '', match)
        match = re.sub(r'<', '(?:<(?:', match)
        match = re.sub(r'>', ')>)', match)
        match = re.sub(r'(?<!\\)\.', '[^>]', match)
        
        # End NLTK contribution
        
        self.id         = id
        self._type      = type
        self._match     = re.compile(match)
        self._squelch   = squelch
        self.after      = after
        self._posguards = []
        self._negguards = []
        
        for guard in guards:
            if guard[0] == '!':
                self._negguards.append(re.compile(guard[1:]))
            else:
                self._posguards.append(re.compile(guard))
    
    def apply(self, sent):
        """
        Applies this rule to the tokenised sentence. The 'after' ordering
        must be checked by the caller to ensure correct rule application.
        
        sent is a list of tuples (token, POS, [timexes])
        
        A list in the same form as sent is returned, with additional timexes
        added to the 3rd element if need be.
        """
        
        # This code is modified from NLTK's text.py for dealing with pattern
        # matching with tokenised strings, under the Apache License 2.0
        
        # Natural Language Toolkit (NLTK) http://www.nltk.org/
        # Copyright (C) 2001-2010 NLTK Project
        # Bird, Steven, Edward Loper and Ewan Klein (2009).
        # Natural Language Processing with Python.  O'Reilly Media Inc.
        
        senttext = ''.join('<'+w+'~'+pos+'>' for (w, pos, ts) in sent)
        
        # End NLTK contribution
        
        # Ensure the guards are satisfied, first any positive ones that are
        # not satisfied means missing no application
        for guard in self._posguards:
            if not guard.search(senttext):
                return sent
        
        # then any negative ones, which if do hit, mean stop processing
        for guard in self._negguards:
            if guard.search(senttext):
                return sent
        
        # Now see if this rule actually matches anything
        for match in self._match.finditer(senttext):
            
            # okay, first we need to find which tokens we matched, can do this
            # by using our token markers
            ti = senttext.count('<', 0, match.start())
            tj = senttext.count('<', 0, match.end()) - 1
            
            if not self._squelch:
                t = timex(self._type) # only create a new timex if not squelching
            
            for i in range(len(sent)):
                # now get all tokens in the range and add the new timex if needed
                (token, pos, ts) = sent[i]
                if i >= ti and i <= tj:
                    if self._squelch:
                        # in the case of this being a squelch rule, remove the
                        # timexes
                        ts = []
                    else:
                        # otherwise add the new timex to the list of timexes
                        # associated with this token
                        ts.append(t)
                
                sent[i] = (token, pos, ts)
        
        return sent