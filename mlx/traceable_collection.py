'''
Storage classes for collection of traceable items
'''

import json
from mlx.traceable_item import TraceableItem
from mlx.traceability_exception import TraceabilityException, MultipleTraceabilityExceptions


class TraceableCollection(object):
    '''
    Storage for a collection of TraceableItems
    '''

    NO_RELATION_STR = ''

    def __init__(self):
        '''Initializer for container of traceable items'''
        self.relations = {}
        self.items = {}

    def add_relation_pair(self, forward, reverse=NO_RELATION_STR):
        '''
        Add a relation pair to the collection

        Args:
            forward (str): Keyword for the forward relation
            reverse (str): Keyword for the reverse relation, or NO_RELATION_STR for external relations
        '''
        # Link forward to reverse relation
        self.relations[forward] = reverse
        # Link reverse to forward relation
        if reverse != self.NO_RELATION_STR:
            self.relations[reverse] = forward

    def get_reverse_relation(self, forward):
        '''
        Get the matching reverse relation

        Args:
            forward (str): Keyword for the forward relation
        Returns:
            str: Keyword for the matching reverse relation, or None
        '''
        if forward in self.relations:
            return self.relations[forward]
        return None

    def iter_relations(self):
        '''
        Iterate over available relations: sorted

        Returns:
            Sorted iterator over available relations in the collection
        '''
        return sorted(self.relations.keys())

    def add_item(self, item):
        '''
        Add a TraceableItem to the list

        Args:
            item (TraceableItem): Traceable item to add
        '''
        itemid = item.get_id()
        # If the item already exists ...
        if itemid in self.items:
            olditem = self.items[itemid]
            # ... and it's not a placeholder, log an error
            if not olditem.placeholder:
                raise TraceabilityException('duplicating {itemid}'.format(itemid=itemid), item.get_document())
            # ... otherwise, update the item with new content
            else:
                olditem.update(item)
        # Otherwise (item doesn't exist), add it
        else:
            self.items[item.get_id()] = item

    def get_item(self, itemid):
        '''
        Get a TraceableItem from the list

        Args:
            itemid (str): Identification of traceable item to get
        Returns:
            TraceableItem: Object for traceable item
        '''
        if self.has_item(itemid):
            return self.items[itemid]
        return None

    def iter_items(self):
        '''
        Iterate over items: sorted identification

        Returns:
            Sorted iterator over identification of the items in the collection
        '''
        return sorted(self.items.keys())

    def has_item(self, itemid):
        '''
        Verify if a item with given id is in the collection

        Args:
            itemid (str): Identification of item to look for
        Returns:
            bool: True if the given itemid is in the collection, false otherwise
        '''
        return itemid in self.items

    def add_relation(self, sourceid, relation, targetid):
        '''
        Add relation between two items

        The function adds the forward and the automatic reverse relation.

        Args:
            sourceid (str): ID of the source item
            relation (str): Relation between source and target item
            targetid (str): ID of the target item
        '''
        # Fail if source item is unknown
        if sourceid not in self.items:
            raise ValueError('Source item {name} not known'.format(name=sourceid))
        source = self.items[sourceid]
        # Error if relation is unknown
        if relation not in self.relations:
            raise TraceabilityException('Relation {name} not known'.format(name=relation), source.get_document())
        # Add forward relation
        source.add_target(relation, targetid)
        # When reverse relation exists, continue to create/adapt target-item
        reverse_relation = self.get_reverse_relation(relation)
        if reverse_relation:
            # Add placeholder if target item is unknown
            if targetid not in self.items:
                tgt = TraceableItem(targetid, True)
                self.add_item(tgt)
            # Add reverse relation to target-item
            self.items[targetid].add_target(reverse_relation, sourceid, implicit=True)

    def export(self, fname):
        '''
        Export collection content

        Args:
            fname (str): Path to the json file to export
        '''
        with open(fname, 'w') as outfile:
            data = []
            for itemid in self.iter_items():
                item = self.get_item(itemid)
                data.append(item.to_dict())
            json.dump(data, outfile, indent=4, sort_keys=True)

    def self_test(self, docname=None):
        '''
        Perform self test on collection content

        Args:
            docname (str): Document on which to run the self test, None for all.
        '''
        errors = []
        # Having no valid relations, is invalid
        if not self.relations:
            raise TraceabilityException('No relations configured', 'configuration')
        # Validate each item
        for itemid in self.items:
            item = self.get_item(itemid)
            # Only for relevant items, filtered on document name
            if docname is not None and item.get_document() != docname and item.get_document() is not None:
                continue
            # On item level
            try:
                item.self_test()
            except TraceabilityException as e:
                errors.append(e)
            # targetted items shall exist, with automatic reverse relation
            for relation in self.relations:
                # Exception: no reverse relation (external links)
                rev_relation = self.get_reverse_relation(relation)
                if rev_relation == self.NO_RELATION_STR:
                    continue
                for tgt in item.iter_targets(relation):
                    # Target item exists?
                    if tgt not in self.items:
                        errors.append(TraceabilityException('''{source} {relation} {target},
                                      but {target} is not known'''.format(source=itemid,
                                                                          relation=relation,
                                                                          target=tgt),
                                      item.get_document()))
                        continue
                    # Reverse relation exists?
                    target = self.get_item(tgt)
                    if itemid not in target.iter_targets(rev_relation):
                        errors.append(TraceabilityException('''No automatic reverse relation:
                                      {source} {relation} {target}'''.format(source=tgt,
                                                                             relation=rev_relation,
                                                                             target=itemid),
                                      item.get_document()))
        if errors:
            raise MultipleTraceabilityExceptions(errors)

    def __str__(self):
        '''
        Convert object to string
        '''
        retval = 'Available relations:'
        for relation in self.relations:
            reverse = self.get_reverse_relation(relation)
            retval += '\t{forward}: {reverse}\n'.format(forward=relation, reverse=reverse)
        for itemid in self.items:
            retval += str(self.items[itemid])
        return retval

    def are_related(self, sourceid, relations, targetid):
        '''
        Check if 2 items are related using a list of relationships

        Placeholders are excluded

        Args:
            - sourceid (str): id of the source item
            - relations (list): list of relations, empty list for wildcard
            - targetid (str): id of the target item
        Returns:
            (boolean) True if both items are related through the given relationships, false otherwise
        '''
        if sourceid not in self.items:
            return False
        source = self.items[sourceid]
        if not source or source.is_placeholder():
            return False
        if targetid not in self.items:
            return False
        target = self.items[targetid]
        if not target or target.is_placeholder():
            return False
        if not relations:
            relations = self.iter_relations()
        return self.items[sourceid].is_related(relations, targetid)

    def get_items(self, regex, attributes={}):
        '''
        Get all items that match a given regular expression

        Placeholders are excluded

        Args:
            - regex (str): Regex to match the items in this collection against
            - attributes (dict): Dictionary with attribute-regex pairs to match the items in this collection against
        Returns:
            A sorted list of item-id's matching the given regex
        '''
        matches = []
        for itemid in self.items:
            if self.items[itemid].is_placeholder():
                continue
            if self.items[itemid].is_match(regex) and self.items[itemid].attributes_match(attributes):
                matches.append(itemid)
        matches.sort()
        return matches
