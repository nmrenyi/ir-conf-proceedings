def save_file(df, output_path, file_type):
    if file_type == 'tsv':
        df.to_csv(output_path, sep='\t', index=False)
    elif file_type == 'md':
        with open(output_path, 'w') as f:
            f.write(df[['title', 'authors', 'session', 'abstract', 'url']].to_markdown(
                index=False).replace('   ', ''))  # remove redundant whitespace to shrink the file size
    else:
        raise ValueError('Unsupported file type: {}'.format(file_type))
    print('output saved to {}'.format(output_path))
