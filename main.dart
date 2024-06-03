import 'dart:async';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Document Search',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const SearchScreen(),
    );
  }
}

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  SearchScreenState createState() => SearchScreenState();
}

class SearchScreenState extends State<SearchScreen> {
  final TextEditingController _searchController = TextEditingController();

  int withEmbedding = 1;
  int withoutEmbedding = 2;

  final int _dataset1 = 1;
  final int _dataset2 = 2;

  int _selectedDataset = 1;
  int _selectedEmbedding = 1;
  List<String> _filteredDocuments = [];
  bool _isLoading = false;
  Timer? _searchDelay;

  @override
  void initState() {
    super.initState();
    _selectedDataset = _dataset1;
    _selectedEmbedding = withEmbedding;
    _filteredDocuments = [];
  }

  Future<void> _searchDocuments(String query) async {
    final datasetId = _selectedDataset == _dataset1 ? '1' : '2';
    final optionId = _selectedEmbedding == withEmbedding ? '1' : '2';
    final url = 'http://10.0.2.2:8000/$datasetId/$optionId';

    setState(() {
      _isLoading = true;
      _filteredDocuments = [];
    });

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'text': query}),
      );
      if (response.statusCode == 200) {
        final List<dynamic> results = json.decode(response.body)['result'];

        setState(() {
          _filteredDocuments = results.cast<String>();
          if (query.isEmpty) _filteredDocuments = [];
        });
      } else {
        setState(() {
          _filteredDocuments = ['Error: ${response.reasonPhrase}'];
        });
      }
    } catch (error) {
      setState(() {
        _filteredDocuments = ['Error: $error'];
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _filterDocuments(String query) {
    _searchDelay?.cancel(); // Cancel the previous timer
    _searchDelay = Timer(const Duration(seconds: 1), () {
      _searchDocuments(query);
    });
  }

  void _onDatasetChanged(int newDataset) {
    setState(() {
      _selectedDataset = newDataset;
      _filterDocuments(_searchController.text);
    });
  }

  void _onEmbeddingChanged(int newDataset) {
    setState(() {
      _selectedEmbedding = newDataset;
      _filterDocuments(_searchController.text);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.grey[300],
        title: const Text('Search Documents'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            // Dropdown to select dataset
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                DropdownButton<int>(
                  value: _selectedEmbedding,
                  items: [
                    DropdownMenuItem(
                      value: withEmbedding,
                      child: const Text('With Embedding'),
                    ),
                    DropdownMenuItem(
                      value: withoutEmbedding,
                      child: const Text('Without Embedding'),
                    ),
                  ],
                  onChanged: (newValue) {
                    if (newValue != null) {
                      _onEmbeddingChanged(newValue);
                    }
                  },
                ),
                DropdownButton<int>(
                  value: _selectedDataset,
                  items: [
                    DropdownMenuItem(
                      value: _dataset1,
                      child: const Text('Antique'),
                    ),
                    DropdownMenuItem(
                      value: _dataset2,
                      child: const Text('Lotte'),
                    ),
                  ],
                  onChanged: (newValue) {
                    if (newValue != null) {
                      _onDatasetChanged(newValue);
                    }
                  },
                ),
              ],
            ),
            TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: 'Search',
                suffixIcon: IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () {
                    _searchController.clear();
                    _filterDocuments('');
                  },
                ),
              ),
              onChanged: (query) {
                {
                  _filterDocuments(query);
                }
              },
            ),
            Expanded(
              child: Stack(
                children: [
                  ListView.builder(
                    itemCount: _filteredDocuments.length,
                    itemBuilder: (context, index) {
                      return ListTile(
                        title: Text(_filteredDocuments[index].length > 35
                            ? '${_filteredDocuments[index].substring(0, 35)}...'
                            : _filteredDocuments[index]),
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => DocumentDetailScreen(
                                document: _filteredDocuments[index],
                              ),
                            ),
                          );
                        },
                      );
                    },
                  ),
                  if (_isLoading)
                    const Center(
                      child: CircularProgressIndicator(),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class DocumentDetailScreen extends StatelessWidget {
  final String document;

  const DocumentDetailScreen({super.key, required this.document});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.grey[300],
        title: const Text('Details'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Text(document),
        ),
      ),
    );
  }
}
