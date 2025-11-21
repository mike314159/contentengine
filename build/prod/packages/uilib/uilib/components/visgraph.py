from ..basecomponents import Component

class VisGraph(Component):
    def __init__(self):
        self.next_id = 1
        self.nodes = {}
        self.edges = {}
        self.node_key_to_id = {}

    #         s = '''
    # ahoy_visits-->agg_fact_user_visit;
    # user_events_visits_elt-->ahoy_visits;
    # user_events_sf-->user_events_visits_elt;
    # wait_for_segment_user_data-->user_events_sf;
    # segment_load_to_redshift-->agg_fact_user_visit;
    # searches-->agg_fact_user_visit;
    # fact_event_visit-->agg_fact_user_visit;
    # segment_load_to_redshift-->fact_event_visit;
    # fact_visitor_user-->agg_fact_user_visit;
    # orders-->fact_visitor_user;
    # ahoy_visits-->fact_visitor_user;
    #         '''
    #
    #         lines = s.split(";")
    #         for line in lines:
    #             parts = line.split("-->")
    #             if len(parts) == 2:
    #                 left = parts[0].strip()
    #                 right = parts[1].strip()
    #                 self.add_node(left, left)
    #                 self.add_node(right, right)
    #                 self.add_upstream_edge(right, left)

    def get_id_from_key(self, key):
        if key in self.node_key_to_id.keys():
            return self.node_key_to_id[key]
        else:
            return None

    def add_node(self, key, label):

        if key not in self.node_key_to_id.keys():
            self.node_key_to_id[key] = self.next_id
            self.next_id += 1

        id = self.node_key_to_id[key]
        if id not in self.nodes.keys():
            self.nodes[id] = label
        #if upstream_id not in self.nodes.keys():
        #    self.nodes[upstream_id] = upstream_label

    def add_upstream_edge(self, key, upstream_key):

        id = self.get_id_from_key(key)
        upstream_id = self.get_id_from_key(upstream_key)
        if (id is None) or (upstream_id) is None:
            return

        if upstream_id not in self.edges.keys():
            self.edges[upstream_id] = set()
        self.edges[upstream_id].add(id)

    def render(self, css_id):

        start = "<script type='text/javascript'>"
        nodes = self.get_nodes()
        edges = self.get_edges()
        network = self.get_network(css_id)
        end = "</script>"
        js = start + nodes + edges + network + end
        html = "<div id='%s' width='600px' height='800px'></div>" % css_id
        return (html, js)

        # chart_html = "<div id='%s' style='width: %s'></div>" % (css_id, width)
        # footer_scripts = """
        #     <script type="text/javascript">
        #       g = new Dygraph(
        #         document.getElementById("%s"),
        #         "%s");
        #     </script>
        # """ % (
        #     css_id,
        #     data_url,
        # )
        # return (chart_html, footer_scripts)

    def get_nodes(self):
        start = "\nvar nodes = new vis.DataSet([\n"
        n = []
        for id in self.nodes.keys():
            n.append("{id: %s, label: '%s'}" % (id, self.nodes[id]))
        nodes_js = ','.join(n)
        end = "\n]);\n"
        js = start + nodes_js + end
        return js

    def get_edges(self):
        start = "var edges = new vis.DataSet(["
        end = "]);\n"
        n = []
        for src_id in self.edges.keys():
            for dest_id in self.edges[src_id]:
                n.append("{from: %s, to: '%s'}" % (src_id, dest_id))
        edges_js = ','.join(n)
        js = start + edges_js + end
        return js

        # edges = '''
        #   var edges = new vis.DataSet([
        #     {from: 1, to: 3}
        #   ]);
        # '''
        # return edges

    def get_network(self, css_id):
        network = '''
          var container = document.getElementById('%s');
          var data = {
            nodes: nodes,
            edges: edges
          };
          var options = {
            "interaction": {
                zoomView: false
            },
            "edges": {
               arrows: {
                    to: {
                        enabled: true
                    }
                }
            },
            "nodes": {
               shape: 'dot'
            },
            "layout": {
               hierarchical: {
                    enabled: true,
                    direction: 'LR',
                    sortMethod: 'directed',
                    levelSeparation: 150,
                    nodeSpacing: 400,
                    shakeTowards: 'leaves'
               }
            }
          };
          var network = new vis.Network(container, data, options);
        ''' % css_id
        return network

#         n = '''
# <script type="text/javascript">
#   // create an array with nodes
#   var nodes = new vis.DataSet([
#     {id: 1, label: 'Node 1'},
#     {id: 2, label: 'Node 2'},
#     {id: 3, label: 'Node 3'},
#     {id: 4, label: 'Node 4'},
#     {id: 5, label: 'Node 5'}
#   ]);
#
#   // create an array with edges
#   var edges = new vis.DataSet([
#     {from: 1, to: 3},
#     {from: 1, to: 2},
#     {from: 2, to: 4},
#     {from: 2, to: 5},
#     {from: 3, to: 3}
#   ]);
#
#   // create a network
#   var container = document.getElementById('mynetwork');
#   var data = {
#     nodes: nodes,
#     edges: edges
#   };
#   var options = {};
#   var network = new vis.Network(container, data, options);
# </script>
#         '''
    def get_css_links(self):
        return "" #<link rel='stylesheet' src='/static/dygraph/dygraph.css' />"

    def get_head_scripts(self):
        return "<script type='text/javascript' src='https://unpkg.com/vis-network/standalone/umd/vis-network.min.js'></script>"
    
    @classmethod
    def example(cls):
        graph = cls()
        # Add some sample nodes and edges
        graph.add_node("node1", "Start")
        graph.add_node("node2", "Process")
        graph.add_node("node3", "End")
        graph.add_edge("node1", "node2")
        graph.add_edge("node2", "node3")
        return graph
