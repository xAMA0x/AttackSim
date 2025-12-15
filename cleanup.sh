#!/bin/bash
# Script de nettoyage pour AttackSim

echo "🧹 Nettoyage d'AttackSim..."

# Nettoyage des fichiers Python
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Nettoyage des rapports anciens (garde les 5 plus récents)
echo "📄 Nettoyage des anciens rapports..."
cd reports/ 2>/dev/null || mkdir -p reports/

# Garde seulement les 5 fichiers PNG les plus récents
ls -t *.png 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
# Garde seulement les 5 fichiers MD les plus récents  
ls -t *.md 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true

cd ..

# Nettoyage des fichiers data temporaires
echo "🗂️  Nettoyage des fichiers data temporaires..."
cd data/ 2>/dev/null || true
rm -f my_* *.tmp 2>/dev/null || true
cd .. 2>/dev/null || true

echo "✅ Nettoyage terminé !"
echo ""
echo "Structure conservée:"
echo "  📁 data/ - Fichiers d'exemple préservés"  
echo "  📁 reports/ - 5 rapports les plus récents conservés"
